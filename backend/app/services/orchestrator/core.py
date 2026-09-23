import time
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.domain import Scene, ScenePair, ExecutionTrace
from app.services.orchestrator.tools import TOOL_REGISTRY
from app.services.orchestrator.verifier import GisVerifyTool
from geoalchemy2.shape import to_shape
from shapely.geometry import box
import os
from app.core.config import settings

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self, db: Session):
        self.db = db
        # Add verifier to local registry copy for this orchestrator run
        self.tool_registry = dict(TOOL_REGISTRY)
        self.tool_registry["gis_verify"] = GisVerifyTool()
        
    def _get_absolute_path(self, path: str) -> str:
        if not path:
            return ""
        if not path.startswith('/'):
            return os.path.join(os.getenv("STORAGE_PATH", "/app/storage"), path)
        return path

    def generate_plan(self, scene: Optional[Scene], pair: Optional[ScenePair], query_text: str) -> List[Dict[str, Any]]:
        plan = []
        
        # Rule 1: Single Scene
        if scene:
            # Rejection rule for SAR-only
            if scene.sensor_type == 'sar':
                raise ValueError("SAR-only VQA is unsupported in this version.")
                
            # If query contains "segment", trigger the Segmentation Stub Tool to fail loudly
            if "segment" in query_text.lower():
                plan.append({
                    "tool": "segmentation",
                    "params": {}
                })
                
            # Optical VQA
            bounds_geom = to_shape(scene.bounds)
            scene_bounds = list(bounds_geom.bounds) # [minx, miny, maxx, maxy]
            plan.append({
                "tool": "vqa",
                "params": {
                    "image_path": self._get_absolute_path(scene.storage_path),
                    "query_text": query_text,
                    "scene_bounds": scene_bounds
                }
            })
            plan.append({
                "tool": "gis_verify",
                "params": {
                    "scene_bounds": scene_bounds
                } # Will be populated with answer_text and bboxes dynamically during execution
            })
            return plan
            
        # Rule 2/3: Scene Pair
        if pair:
            if pair.coregistration_status != "done":
                raise ValueError("Co-registration not complete for this pair")
                
            before_path = self._get_absolute_path(pair.before_aligned_path)
            after_path = self._get_absolute_path(pair.after_aligned_path)
            
            # Use before_scene bounds for GIS as they are co-registered to it
            bounds_geom = to_shape(pair.before_scene.bounds)
            scene_bounds = list(bounds_geom.bounds)
            
            opt_opt = pair.before_scene.sensor_type == 'optical' and pair.after_scene.sensor_type == 'optical'
            opt_sar = (pair.before_scene.sensor_type == 'optical' and pair.after_scene.sensor_type == 'sar') or \
                      (pair.before_scene.sensor_type == 'sar' and pair.after_scene.sensor_type == 'optical')
                      
            if opt_opt:
                # Rule 2: Temporal Change Detection
                plan.append({
                    "tool": "change_detection",
                    "params": {
                        "before_image_path": before_path,
                        "after_image_path": after_path,
                        "scene_bounds": scene_bounds
                    }
                })
            elif opt_sar:
                # Rule 3: Multi-Sensor Fusion
                if pair.before_scene.sensor_type == 'optical':
                    opt_path = before_path
                    sar_path = after_path
                else:
                    opt_path = after_path
                    sar_path = before_path
                    
                plan.append({
                    "tool": "fusion",
                    "params": {
                        "optical_image_path": opt_path,
                        "sar_image_path": sar_path,
                        "query_text": query_text,
                        "scene_bounds": scene_bounds
                    }
                })
            else:
                raise ValueError("SAR-SAR change detection is not currently supported.")
                
            plan.append({
                "tool": "gis_verify",
                "params": {
                    "scene_bounds": scene_bounds
                }
            })
            return plan
            
        raise ValueError("Must provide either scene or pair")

    def execute(self, query_id: int, scene_id: Optional[int], scene_pair_id: Optional[int], query_text: str) -> Dict[str, Any]:
        start_time = time.time()
        scene = None
        pair = None
        
        if scene_id:
            scene = self.db.query(Scene).filter(Scene.id == scene_id).first()
        elif scene_pair_id:
            pair = self.db.query(ScenePair).filter(ScenePair.id == scene_pair_id).first()
            
        try:
            plan = self.generate_plan(scene, pair, query_text)
        except ValueError as e:
            # Handle explicit rejections
            return {"error": str(e), "trace_id": None}
            
        steps = []
        final_answer = ""
        final_bboxes = []
        final_confidence = None
        final_mask_path = ""
        verification_result = None
        
        # Execute Plan
        for step in plan:
            tool_name = step["tool"]
            params = step["params"]
            
            # Inject previous step results into GIS Verifier
            if tool_name == "gis_verify":
                params["answer_text"] = final_answer
                params["bounding_boxes"] = final_bboxes
                
            tool_instance = self.tool_registry.get(tool_name)
            if not tool_instance:
                raise ValueError(f"Tool {tool_name} not found in registry")
                
            step_start = time.time()
            result = tool_instance.run(params)
            step_latency = int((time.time() - step_start) * 1000)
            
            if result.error:
                # Fail loudly
                steps.append({
                    "tool": tool_name,
                    "status": "error",
                    "error": result.error,
                    "latency_ms": step_latency
                })
                return {"error": f"Tool {tool_name} failed: {result.error}", "trace_id": None}
                
            if tool_name == "gis_verify":
                verification_result = result.output_data
            else:
                final_answer = result.output_data.get("answer_text", "")
                final_bboxes = result.output_data.get("bounding_boxes", [])
                final_mask_path = result.output_data.get("mask_path", "")
                final_confidence = result.confidence
                
            steps.append({
                "tool": tool_name,
                "status": "success",
                "params": params,
                "output": result.output_data,
                "latency_ms": step_latency
            })
            
        total_latency = int((time.time() - start_time) * 1000)
        
        # Log to ExecutionTrace
        trace = ExecutionTrace(
            query_id=query_id,
            plan_json=plan,
            steps_json=steps,
            verification_result_json=verification_result,
            total_latency_ms=total_latency
        )
        self.db.add(trace)
        self.db.commit()
        self.db.refresh(trace)
        
        return {
            "trace_id": trace.id,
            "answer_text": final_answer,
            "bounding_boxes": final_bboxes,
            "mask_path": final_mask_path,
            "confidence": final_confidence,
            "verification": verification_result
        }
