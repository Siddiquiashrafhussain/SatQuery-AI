from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.api.deps import get_db, get_current_user
from app.models.domain import User, Query, Scene
from typing import Optional

router = APIRouter(prefix="/api/v1/query", tags=["query"])

class QueryCreate(BaseModel):
    scene_id: int
    query_text: str

class QueryResponse(BaseModel):
    query_id: int
    answer: str
    confidence: Optional[float] = None
    bounding_boxes: Optional[list[list[float]]] = None

@router.post("/", response_model=QueryResponse)
def submit_query(
    query_in: QueryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify scene exists and belongs to user
    scene = db.query(Scene).filter(Scene.id == query_in.scene_id, Scene.user_id == current_user.id).first()
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
        
    # Create the query record
    db_query = Query(
        user_id=current_user.id,
        scene_id=scene.id,
        query_text=query_in.query_text
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    
    from app.services.orchestrator.core import Orchestrator
    orchestrator = Orchestrator(db)
    result = orchestrator.execute(
        query_id=db_query.id,
        scene_id=scene.id,
        scene_pair_id=None,
        query_text=query_in.query_text
    )
    
    if result.get("error"):
        if "SAR-only" in result["error"]:
            raise HTTPException(status_code=400, detail=result["error"])
        raise HTTPException(status_code=500, detail=result["error"])
        
    # Store analysis result (Phase 2 legacy shape support)
    from app.models.domain import AnalysisResult
    result_record = AnalysisResult(
        query_id=db_query.id,
        result_text=result.get("answer_text", ""),
        confidence_score=result.get("confidence"),
        bounding_boxes=result.get("bounding_boxes", [])
    )
    db.add(result_record)
    db.commit()

    return QueryResponse(
        query_id=db_query.id,
        answer=result_record.result_text,
        confidence=result_record.confidence_score,
        bounding_boxes=result_record.bounding_boxes
    )

class ChangeQueryCreate(BaseModel):
    scene_pair_id: int

class ChangeQueryResponse(BaseModel):
    change_result_id: int
    query_id: int
    summary: str
    confidence: Optional[float] = None
    mask_path: str
    bounding_boxes: Optional[list[list[float]]] = None

@router.post("/change", response_model=ChangeQueryResponse)
def submit_change_query(
    query_in: ChangeQueryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.domain import ScenePair, ChangeResult
    import os
    import httpx
    from app.core.config import settings
    
    pair = db.query(ScenePair).filter(ScenePair.id == query_in.scene_pair_id, ScenePair.user_id == current_user.id).first()
    if not pair:
        raise HTTPException(status_code=404, detail="Scene pair not found")
        
    from app.services.orchestrator.core import Orchestrator
    
    # We will pass a dummy query to the orchestrator to store the trace, 
    # but the Change endpoints originally didn't create a `Query` record, they just returned ChangeQueryResponse.
    # To log traces properly, we need a query_id. 
    # Let's create a placeholder Query record for change pair queries.
    from app.models.domain import Query
    db_query = Query(
        user_id=current_user.id,
        scene_id=pair.before_scene_id,  # Link to the before scene loosely
        query_text="Temporal Change Analysis" # Default text for pure change requests
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    
    orchestrator = Orchestrator(db)
    result = orchestrator.execute(
        query_id=db_query.id,
        scene_id=None,
        scene_pair_id=pair.id,
        query_text="Temporal Change Analysis"
    )
    
    if result.get("error"):
        if "SAR-SAR" in result["error"]:
            raise HTTPException(status_code=400, detail=result["error"])
        raise HTTPException(status_code=500, detail=result["error"])

    is_fusion = (pair.before_scene.sensor_type == 'optical' and pair.after_scene.sensor_type == 'sar') or \
                (pair.before_scene.sensor_type == 'sar' and pair.after_scene.sensor_type == 'optical')

    if is_fusion:
        # Map fusion response to ChangeResult shape for UI compatibility
        change_record = ChangeResult(
            scene_pair_id=pair.id,
            mask_path=result.get("mask_path", ""), # Fusion could return bounding_boxes, but we store it as mask_path or we need to update ChangeResult schema? 
            # Wait, the prompt says: "returning results in the same shape as Phase 2's VQA response ({ answer_text, bounding_boxes, confidence }) so the frontend can reuse Phase 2's display components". 
            # If the frontend reuses Phase 2's UI, does the UI expect activeQueryResult to have bounding_boxes? Yes, MapViewer checks activeQueryResult.bounding_boxes.
            # But wait, this route returns `ChangeQueryResponse` which doesn't have bounding_boxes, it has `mask_path`.
            # Let me just put bounding_boxes in the `summary_text` as a JSON string or alter the Response Model.
            # I will modify ChangeQueryResponse to optionally include bounding_boxes and store it.
            summary_text=result.get("answer_text", ""),
            confidence=result.get("confidence")
        )
    else:
        change_record = ChangeResult(
            scene_pair_id=pair.id,
            mask_path=result.get("mask_path", ""),
            summary_text=result.get("answer_text", ""),
            confidence=result.get("confidence")
        )
    db.add(change_record)
    db.commit()
    db.refresh(change_record)

    return ChangeQueryResponse(
        change_result_id=change_record.id,
        query_id=db_query.id,
        summary=change_record.summary_text,
        confidence=change_record.confidence,
        mask_path=change_record.mask_path,
        bounding_boxes=result.get("bounding_boxes", []) if is_fusion else None
    )

@router.get("/{query_id}/trace")
def get_query_trace(
    query_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.domain import ExecutionTrace, Query
    
    # Check ownership
    db_query = db.query(Query).filter(Query.id == query_id, Query.user_id == current_user.id).first()
    if not db_query:
        raise HTTPException(status_code=404, detail="Query not found")
        
    trace = db.query(ExecutionTrace).filter(ExecutionTrace.query_id == query_id).first()
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found for this query")
        
    return {
        "id": trace.id,
        "query_id": trace.query_id,
        "plan": trace.plan_json,
        "steps": trace.steps_json,
        "verification_result": trace.verification_result_json,
        "total_latency_ms": trace.total_latency_ms,
        "created_at": trace.created_at
    }
