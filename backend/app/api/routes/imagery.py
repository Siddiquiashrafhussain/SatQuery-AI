import os
import uuid
import rasterio
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.domain import User, Scene
from app.schemas.domain import SceneResponse
from app.services.storage import storage_backend
from geoalchemy2.shape import from_shape
from shapely.geometry import box

from pydantic import BaseModel
from sqlalchemy import func

router = APIRouter()

class ScenePairCreate(BaseModel):
    before_scene_id: int
    after_scene_id: int

@router.post("/pairs")
def create_scene_pair(
    pair_in: ScenePairCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.domain import ScenePair
    
    before_scene = db.query(Scene).filter(Scene.id == pair_in.before_scene_id, Scene.user_id == current_user.id).first()
    after_scene = db.query(Scene).filter(Scene.id == pair_in.after_scene_id, Scene.user_id == current_user.id).first()
    
    if not before_scene or not after_scene:
        raise HTTPException(status_code=404, detail="One or both scenes not found")
        
    # Check intersection using PostGIS ST_Intersects
    intersects = db.query(func.ST_Intersects(before_scene.bounds, after_scene.bounds)).scalar()
    if not intersects:
        raise HTTPException(status_code=400, detail="Scenes do not geographically overlap. Cannot perform change analysis.")
        
    scene_pair = ScenePair(
        user_id=current_user.id,
        before_scene_id=before_scene.id,
        after_scene_id=after_scene.id
    )
    db.add(scene_pair)
    db.commit()
    db.refresh(scene_pair)
    
    return {
        "id": scene_pair.id,
        "before_scene_id": scene_pair.before_scene_id,
        "after_scene_id": scene_pair.after_scene_id,
        "coregistration_status": scene_pair.coregistration_status
    }

@router.post("/upload", response_model=SceneResponse)
async def upload_scene(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.lower().endswith(('.tif', '.tiff')):
        raise HTTPException(status_code=400, detail="Only GeoTIFF files are allowed")

    # Generate unique filename and save via chunked storage abstraction
    filename = f"{uuid.uuid4()}_{file.filename}"
    saved_path = await storage_backend.save_upload(file, filename)

    try:
        # Validate and extract metadata with rasterio
        with rasterio.open(saved_path) as src:
            crs_str = src.crs.to_string() if src.crs else None
            bands = src.count
            res_x, res_y = src.res
            resolution = (res_x + res_y) / 2.0
            
            # bounds as shapely Polygon
            bbox = box(*src.bounds)
            # Make sure it's in 4326 for PostGIS (assuming EPSG:4326 for simplicity in Phase 0)
            # In a real app we'd reproject bounds to 4326
            geom = from_shape(bbox, srid=4326)

            # Sensor type detection heuristic
            sensor_type = "optical"
            sar_polarization = None
            sar_acquisition_mode = None
            
            upper_filename = file.filename.upper()
            if upper_filename.startswith("S1A") or upper_filename.startswith("S1B") or bands <= 2:
                sensor_type = "sar"
                # Example Sentinel-1: S1A_IW_GRDH_1SDV_...
                parts = upper_filename.split("_")
                if len(parts) > 3:
                    sar_acquisition_mode = parts[1] # e.g. IW
                    pol_str = parts[3]
                    if len(pol_str) >= 4:
                        if pol_str[3] == 'V':
                            sar_polarization = 'VV/VH' if pol_str[2] == 'D' else 'VV'
                        elif pol_str[3] == 'H':
                            sar_polarization = 'HH/HV' if pol_str[2] == 'D' else 'HH'

    except rasterio.errors.RasterioIOError:
        os.remove(saved_path)
        raise HTTPException(status_code=400, detail="Invalid GeoTIFF file")

    # Save to DB
    scene = Scene(
        user_id=current_user.id,
        filename=file.filename,
        storage_path=saved_path,
        crs=crs_str,
        bounds=geom,
        bands=bands,
        resolution=resolution,
        sensor_type=sensor_type,
        sar_polarization=sar_polarization,
        sar_acquisition_mode=sar_acquisition_mode
    )
    db.add(scene)
    db.commit()
    db.refresh(scene)
    
    return {
        "id": scene.id,
        "user_id": scene.user_id,
        "filename": scene.filename,
        "crs": scene.crs,
        "bands": scene.bands,
        "resolution": scene.resolution,
        "sensor_type": scene.sensor_type,
        "preprocessing_status": scene.preprocessing_status,
        "uploaded_at": scene.uploaded_at,
        "bbox": list(src.bounds) if 'src' in locals() else None
    }
