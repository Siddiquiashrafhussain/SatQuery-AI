from typing import Optional, Protocol
from pydantic import BaseModel
import httpx
import os
import logging

logger = logging.getLogger(__name__)

class ToolResult(BaseModel):
    output_data: dict
    confidence: Optional[float] = None
    raw_response: dict
    error: Optional[str] = None

class BaseTool(Protocol):
    def run(self, params: dict) -> ToolResult:
        ...

class VqaTool:
    def run(self, params: dict) -> ToolResult:
        image_path = params.get("image_path")
        query_text = params.get("query_text")
        
        if not image_path:
            return ToolResult(output_data={}, raw_response={}, error="Missing image_path")
            
        ml_url = os.getenv("ML_SERVICE_URL", "http://ml:8001")
        try:
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(f"{ml_url}/infer", json={
                    "image_path_or_url": image_path,
                    "query_text": query_text
                })
                resp.raise_for_status()
                data = resp.json()
                
            return ToolResult(
                output_data={"answer_text": data.get("answer_text", ""), "bounding_boxes": data.get("bounding_boxes", [])},
                confidence=data.get("confidence"),
                raw_response=data
            )
        except Exception as e:
            logger.error(f"VqaTool failed: {e}")
            return ToolResult(output_data={}, raw_response={}, error=str(e))

class ChangeDetectionTool:
    def run(self, params: dict) -> ToolResult:
        before_path = params.get("before_image_path")
        after_path = params.get("after_image_path")
        
        if not before_path or not after_path:
            return ToolResult(output_data={}, raw_response={}, error="Missing image paths")
            
        cd_url = os.getenv("CHANGE_DETECTION_URL", "http://change_detection:8002")
        try:
            with httpx.Client(timeout=120.0) as client:
                resp = client.post(f"{cd_url}/detect-change", json={
                    "before_image_path": before_path,
                    "after_image_path": after_path
                })
                resp.raise_for_status()
                data = resp.json()
                
            return ToolResult(
                output_data={"answer_text": data.get("change_summary_text", ""), "mask_path": data.get("change_mask_path", "")},
                confidence=data.get("confidence"),
                raw_response=data
            )
        except Exception as e:
            logger.error(f"ChangeDetectionTool failed: {e}")
            return ToolResult(output_data={}, raw_response={}, error=str(e))

class FusionTool:
    def run(self, params: dict) -> ToolResult:
        optical_path = params.get("optical_image_path")
        sar_path = params.get("sar_image_path")
        query_text = params.get("query_text", "")
        
        if not optical_path or not sar_path:
            return ToolResult(output_data={}, raw_response={}, error="Missing image paths")
            
        fusion_url = os.getenv("FUSION_URL", "http://fusion:8003")
        try:
            with httpx.Client(timeout=120.0) as client:
                resp = client.post(f"{fusion_url}/fuse-infer", json={
                    "optical_image_path": optical_path,
                    "sar_image_path": sar_path,
                    "query_text": query_text
                })
                resp.raise_for_status()
                data = resp.json()
                
            return ToolResult(
                output_data={"answer_text": data.get("answer_text", ""), "bounding_boxes": data.get("bounding_boxes", [])},
                confidence=data.get("confidence"),
                raw_response=data
            )
        except Exception as e:
            logger.error(f"FusionTool failed: {e}")
            return ToolResult(output_data={}, raw_response={}, error=str(e))

class SegmentationStubTool:
    def run(self, params: dict) -> ToolResult:
        return ToolResult(
            output_data={},
            raw_response={},
            error="Not Implemented: Segmentation tool is a future enhancement."
        )

# Tool Registry
TOOL_REGISTRY = {
    "vqa": VqaTool(),
    "change_detection": ChangeDetectionTool(),
    "fusion": FusionTool(),
    "segmentation": SegmentationStubTool(),
}
