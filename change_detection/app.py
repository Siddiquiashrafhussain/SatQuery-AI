import os
import time
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import rasterio
import numpy as np
from skimage.filters import threshold_otsu
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SatQuery AI - Change Detection Service")

STORAGE_PATH = os.getenv("STORAGE_PATH", "/app/storage")

class ChangeRequest(BaseModel):
    before_image_path: str
    after_image_path: str

class ChangeResponse(BaseModel):
    change_mask_path: str
    change_summary_text: str
    confidence: float

@app.get("/health")
def health():
    return {"status": "ok", "service": "change_detection"}

@app.post("/detect-change", response_model=ChangeResponse)
def detect_change(req: ChangeRequest):
    start_time = time.time()
    
    try:
        # Load the co-registered images
        with rasterio.open(req.before_image_path) as src_before:
            before_data = src_before.read().astype(np.float32)
            meta = src_before.meta.copy()
            
        with rasterio.open(req.after_image_path) as src_after:
            after_data = src_after.read().astype(np.float32)
            
        if before_data.shape != after_data.shape:
            raise ValueError("Images do not have the same shape. Co-registration may have failed.")
            
        # Change Vector Analysis (CVA) Baseline
        # Calculate Euclidean distance between the spectral vectors
        diff = after_data - before_data
        magnitude = np.sqrt(np.sum(diff**2, axis=0))
        
        # Avoid processing completely empty/nodata regions if possible
        # For simplicity, we just apply Otsu's threshold to the magnitude
        # We ignore pure 0s (nodata) for the threshold calculation
        valid_pixels = magnitude[magnitude > 0]
        if len(valid_pixels) == 0:
            threshold = 0
        else:
            threshold = threshold_otsu(valid_pixels)
            
        # Create binary mask (1 for change, 0 for no change)
        change_mask = (magnitude > threshold).astype(np.uint8)
        
        # Save the mask to storage
        mask_filename = f"change_mask_{uuid.uuid4().hex}.tif"
        mask_path = os.path.join(STORAGE_PATH, mask_filename)
        
        meta.update(count=1, dtype=rasterio.uint8)
        with rasterio.open(mask_path, 'w', **meta) as dst:
            dst.write(change_mask, 1)
            
        # Calculate summary statistics
        total_pixels = change_mask.size
        changed_pixels = np.sum(change_mask)
        change_percentage = (changed_pixels / total_pixels) * 100 if total_pixels > 0 else 0
        
        summary = f"Detected significant change in {change_percentage:.2f}% of the selected region."
        
        # Confidence heuristic: how distinctly bimodal is the magnitude?
        # A simple proxy is to return a high confidence since this is a deterministic baseline.
        confidence = 0.85
        
        latency = time.time() - start_time
        logger.info(f"Change detection completed in {latency:.2f}s. Mask: {mask_filename}")
        
        return ChangeResponse(
            change_mask_path=mask_filename, # relative path
            change_summary_text=summary,
            confidence=confidence
        )
        
    except Exception as e:
        logger.error(f"Change detection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
