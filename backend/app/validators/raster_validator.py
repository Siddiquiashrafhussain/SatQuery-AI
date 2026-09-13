import os
from typing import List
from app.schemas.dataset import ValidationResult
from app.schemas.agent_schema import Modality

class RasterValidator:
    ALLOWED_EXTENSIONS = {'.tif', '.tiff', '.vrt'}

    def validate_single_image(self, file_path: str) -> ValidationResult:
        """
        Safely validates a single remote sensing image.
        Uses structural header inspection rather than arbitrary execution.
        """
        result = ValidationResult(valid=True)
        
        # 1. Safe Path & Extension Check
        if not os.path.exists(file_path):
            result.valid = False
            result.errors.append(f"File not found: {file_path}")
            return result
            
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            result.valid = False
            result.errors.append(f"Invalid file format: {ext}. Allowed: {self.ALLOWED_EXTENSIONS}")
            return result
            
        # 2. Safe Metadata Inspection (using rasterio in production)
        # Wrapped in a try-except block to gracefully handle corrupted TIFFs
        try:
            # STUB: In production, we use Rasterio exclusively for safe header reads:
            # import rasterio
            # with rasterio.open(file_path) as src:
            #     result.crs = str(src.crs)
            #     result.dimensions = [src.width, src.height, src.count]
            #     
            #     # Basic modality heuristic
            #     if src.count > 3:
            #         result.detected_modality = Modality.MULTISPECTRAL
            #     elif src.count == 3:
            #         result.detected_modality = Modality.OPTICAL
            #     else:
            #         result.detected_modality = Modality.SAR
            
            # STUB MOCK DATA
            result.crs = "EPSG:4326"
            result.dimensions = [1024, 1024, 3]
            result.detected_modality = Modality.OPTICAL
            result.metadata = {"driver": "GTiff", "nodata": 0.0}
            
        except Exception as e:
            result.valid = False
            result.errors.append(f"Failed to parse raster metadata safely: {str(e)}")
            
        return result
