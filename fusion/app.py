from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
import rasterio
import numpy as np

app = FastAPI(title="SAR-Optical Fusion Service")

class FusionRequest(BaseModel):
    optical_image_path: str
    sar_image_path: str
    query_text: str = "Describe what you see in this scene."

class FusionResponse(BaseModel):
    answer_text: str
    bounding_boxes: list[list[float]] = []
    confidence: float | None = None

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/fuse-infer", response_model=FusionResponse)
def fuse_infer(req: FusionRequest):
    ml_url = os.getenv("ML_SERVICE_URL", "http://ml:8001")
    
    # 1. Ask the Optical VLM for semantic understanding
    try:
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(f"{ml_url}/infer", json={
                "image_path_or_url": req.optical_image_path,
                "query_text": req.query_text
            })
            resp.raise_for_status()
            opt_data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to query Optical VLM: {str(e)}")
        
    answer_text = opt_data.get("answer_text", "")
    bboxes = opt_data.get("bounding_boxes", [])
    
    if not bboxes:
        return FusionResponse(
            answer_text=f"Optical Analysis: {answer_text}\nSAR Fusion: No specific regions detected by optical model to fuse with SAR.",
            bounding_boxes=[],
            confidence=None # Late-Fusion baseline has no calibrated multimodal confidence
        )
        
    # 2. Extract SAR structural stats for the bounding boxes
    try:
        with rasterio.open(req.sar_image_path) as src:
            width = src.width
            height = src.height
            sar_data = src.read(1) # Assuming single band or first band is what we want for stats
            
        sar_summaries = []
        for i, box in enumerate(bboxes):
            # Florence-2 box format: [x1, y1, x2, y2] normalized 0-1
            x1, y1, x2, y2 = box
            
            # Map normalized coords to SAR pixel grid
            # Since Optical and SAR are co-registered, they share the exact same grid
            px1 = int(x1 * width)
            py1 = int(y1 * height)
            px2 = int(x2 * width)
            py2 = int(y2 * height)
            
            # Ensure within bounds
            px1, px2 = sorted([max(0, min(px1, width-1)), max(0, min(px2, width-1))])
            py1, py2 = sorted([max(0, min(py1, height-1)), max(0, min(py2, height-1))])
            
            if px2 > px1 and py2 > py1:
                region = sar_data[py1:py2, px1:px2]
                mean_db = np.nanmean(region)
                if mean_db > -10:
                    structure = "High structural backscatter (likely solid/built structures)"
                elif mean_db < -20:
                    structure = "Low structural backscatter (likely flat ground/water/smooth surfaces)"
                else:
                    structure = "Moderate backscatter (likely vegetation/mixed surfaces)"
                
                sar_summaries.append(f"Region {i+1}: {mean_db:.1f} dB ({structure}).")
                
    except Exception as e:
        print(f"SAR Extraction Error: {e}")
        sar_summaries = ["Failed to extract SAR statistics due to reading error."]
        
    fused_answer = f"**Optical VLM:** {answer_text}\n\n**SAR Structural Verification:**\n" + "\n".join(sar_summaries)
    
    return FusionResponse(
        answer_text=fused_answer,
        bounding_boxes=bboxes,
        confidence=None
    )
