import os
import time
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import rasterio
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SatQuery AI - ML Service")

# Configuration
MODEL_ID = os.getenv("MODEL_ID", "microsoft/Florence-2-base")
USE_FINETUNED_ADAPTER = os.getenv("USE_FINETUNED_ADAPTER", "false").lower() == "true"
ADAPTER_PATH = os.getenv("ADAPTER_PATH", "/app/training/lora_output")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = None
processor = None

class InferRequest(BaseModel):
    image_path_or_url: str
    query_text: str

class InferResponse(BaseModel):
    answer_text: str
    bounding_boxes: list[list[float]] = []
    confidence: float | None = None

@app.on_event("startup")
def load_model():
    global model, processor
    start_time = time.time()
    logger.info(f"Loading model {MODEL_ID} on {DEVICE}...")
    
    # Load processor
    processor = AutoProcessor.from_pretrained(MODEL_ID, trust_remote_code=True)
    
    # Load model
    dtype = torch.float16 if DEVICE == "cuda" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
        torch_dtype=dtype,
    ).to(DEVICE)
    
    if USE_FINETUNED_ADAPTER and os.path.exists(ADAPTER_PATH):
        logger.info(f"Loading LoRA adapter from {ADAPTER_PATH}")
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, ADAPTER_PATH)
        
    model.eval()
    logger.info(f"Model loaded in {time.time() - start_time:.2f} seconds.")

@app.get("/health")
def health():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ok", "model": MODEL_ID, "device": DEVICE}

def read_image(path: str) -> Image.Image:
    """Reads a GeoTIFF or standard image into a PIL Image."""
    if path.lower().endswith(('.tif', '.tiff')):
        with rasterio.open(path) as src:
            # Read first 3 bands for RGB
            bands = src.count
            if bands >= 3:
                img_data = src.read([1, 2, 3])
                # rasterio reads as (C, H, W). Convert to (H, W, C)
                img_data = np.transpose(img_data, (1, 2, 0))
            else:
                img_data = src.read(1) # single band
                
            # Normalize to 0-255 uint8 if not already
            if img_data.dtype != np.uint8:
                img_data = (255 * (img_data - np.min(img_data)) / (np.max(img_data) - np.min(img_data) + 1e-8)).astype(np.uint8)
                
            return Image.fromarray(img_data)
    else:
        return Image.open(path).convert("RGB")

@app.post("/infer", response_model=InferResponse)
def infer(req: InferRequest):
    start_time = time.time()
    
    try:
        # We assume the path is accessible to the ML service (e.g. shared volume)
        if not os.path.exists(req.image_path_or_url):
            raise HTTPException(status_code=404, detail=f"Image path not found: {req.image_path_or_url}")
            
        image = read_image(req.image_path_or_url)
    except Exception as e:
        logger.error(f"Failed to read image: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to read image: {str(e)}")

    # Florence-2 prompt format for VQA: "<vqa> query"
    prompt = f"<vqa> {req.query_text}"
    
    inputs = processor(text=prompt, images=image, return_tensors="pt").to(DEVICE, model.dtype)
    
    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=128,
            num_beams=3,
        )
        
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    
    # Florence-2 output processing
    # The output contains the answer and potentially <loc_XXX> tokens.
    parsed_answer = processor.post_process_generation(
        generated_text, 
        task="<vqa>", 
        image_size=(image.width, image.height)
    )
    
    # parsed_answer is usually a dict like: {'<vqa>': 'The answer is car'} 
    # For bounding boxes, if it was an Object Detection task, it would return boxes.
    # In VQA, if the answer has locations, post_process_generation tries to extract them.
    # Let's extract them manually or from the parsed result.
    
    raw_answer = parsed_answer.get("<vqa>", generated_text)
    
    # We will just parse the generated text manually for <loc_XXX> tokens to be safe
    import re
    boxes = []
    # Florence-2 boxes are represented as <loc_X> where X is 0-1000
    loc_pattern = r"<loc_(\d+)><loc_(\d+)><loc_(\d+)><loc_(\d+)>"
    matches = re.finditer(loc_pattern, generated_text)
    for match in matches:
        x1, y1, x2, y2 = [int(m) / 1000.0 for m in match.groups()]
        boxes.append([x1, y1, x2, y2])
        
    # Clean the raw answer by removing location tokens
    clean_answer = re.sub(r"<loc_\d+>", "", str(raw_answer)).strip()
    
    # We don't have true confidence for Florence-2 out of the box unless we do logprobs.
    # We'll set it to None as per requirements for base models.
    
    latency = time.time() - start_time
    logger.info(f"Inference completed in {latency:.2f}s. Answer: {clean_answer}")
    
    return InferResponse(
        answer_text=clean_answer,
        bounding_boxes=boxes,
        confidence=None
    )
