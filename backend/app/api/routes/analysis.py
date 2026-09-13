from fastapi import APIRouter
from app.schemas.api import AnalysisRequest, AnalysisResponse
import uuid

router = APIRouter()

@router.post("", response_model=AnalysisResponse)
async def submit_analysis(request: AnalysisRequest):
    """
    Submits a query and dataset for agentic analysis.
    This route ONLY delegates to the orchestration service. It contains NO business logic.
    """
    # STUB: Call Orchestration Service here
    
    return AnalysisResponse(
        job_id=str(uuid.uuid4()),
        status="queued",
        message="Analysis accepted"
    )
