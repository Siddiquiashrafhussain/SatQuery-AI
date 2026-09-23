import os
import time
import rasterio
from rasterio.enums import Resampling
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
import sys
import logging

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.domain import Scene, ScenePair
from app.core.config import settings
from app.services.storage import get_storage_service
from coregister import coregister_scenes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def build_pyramid(input_path: str, output_path: str):
    """
    Simulate a GDAL pyramid building by downsampling.
    In a real scenario we'd use `gdal_retile.py` or rasterio overviews.
    """
    with rasterio.open(input_path) as src:
        # Build overviews (pyramid)
        factors = [2, 4, 8, 16]
        src.build_overviews(factors, Resampling.average)
        src.update_tags(ns='rio_overview', resampling='average')
        logger.info(f"Built pyramid for {input_path}")
        
    # We'll just leave the output as the same file with overviews built.
    if input_path != output_path:
        os.rename(input_path, output_path)

import numpy as np
from scipy.ndimage import median_filter

def preprocess_sar(input_path: str, output_path: str):
    """
    Simulate SAR specific preprocessing: Speckle filtering and dB conversion.
    """
    with rasterio.open(input_path) as src:
        meta = src.meta.copy()
        # SAR is often single band (VV) or dual band (VV, VH)
        data = src.read()
        
    processed_data = np.zeros_like(data, dtype=np.float32)
    meta.update(dtype=rasterio.float32)
    
    for b in range(data.shape[0]):
        band = data[b].astype(np.float32)
        # Apply median filter (Speckle filtering)
        band = median_filter(band, size=3)
        # Apply dB conversion: 10 * log10(x). Avoid log(0)
        # Assuming linear power scale
        band_db = 10 * np.log10(np.where(band <= 0, 1e-10, band))
        processed_data[b] = band_db
        
    with rasterio.open(output_path, 'w', **meta) as dst:
        dst.write(processed_data)
        
    logger.info(f"Processed SAR (Speckle/dB) for {input_path}")

def process_pending_scenes():
    db = SessionLocal()
    try:
        storage = get_storage_service()
        # Find scenes that are pending
        pending_scenes = db.query(Scene).filter(Scene.preprocessing_status == "pending").all()
        for scene in pending_scenes:
            logger.info(f"Processing scene {scene.id}: {scene.filename} (Sensor: {scene.sensor_type})")
            scene.preprocessing_status = "processing"
            db.commit()
            
            try:
                # Local path assumption for Phase 1.
                input_file = storage.get_file_path(scene.storage_path)
                output_file = input_file.replace(".tif", "_processed.tif")
                
                if scene.sensor_type == "sar":
                    preprocess_sar(input_file, output_file)
                else:
                    build_pyramid(input_file, output_file)
                
                scene.storage_path = output_file.replace(settings.STORAGE_PATH + "/", "")
                scene.preprocessing_status = "done"
                db.commit()
                logger.info(f"Successfully processed scene {scene.id}")
            except Exception as e:
                logger.error(f"Error processing scene {scene.id}: {e}")
                scene.preprocessing_status = "failed"
                db.commit()
    finally:
        db.close()

def process_pending_pairs():
    db = SessionLocal()
    try:
        storage = get_storage_service()
        pending_pairs = db.query(ScenePair).filter(ScenePair.coregistration_status == "pending").all()
        for pair in pending_pairs:
            logger.info(f"Processing ScenePair {pair.id}")
            pair.coregistration_status = "processing"
            db.commit()
            
            try:
                before_path = storage.get_file_path(pair.before_scene.storage_path)
                after_path = storage.get_file_path(pair.after_scene.storage_path)
                
                output_before = before_path.replace(".tif", f"_coreg_{pair.id}.tif")
                output_after = after_path.replace(".tif", f"_coreg_{pair.id}.tif")
                
                coregister_scenes(before_path, after_path, output_before, output_after)
                
                pair.before_aligned_path = output_before.replace(settings.STORAGE_PATH + "/", "")
                pair.after_aligned_path = output_after.replace(settings.STORAGE_PATH + "/", "")
                pair.coregistration_status = "done"
                db.commit()
                logger.info(f"Successfully processed ScenePair {pair.id}")
            except Exception as e:
                logger.error(f"Error processing ScenePair {pair.id}: {e}")
                pair.coregistration_status = "failed"
                db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Starting preprocessing worker...")
    while True:
        process_pending_scenes()
        process_pending_pairs()
        time.sleep(10) # Poll every 10 seconds
