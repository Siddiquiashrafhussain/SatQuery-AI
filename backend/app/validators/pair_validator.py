from app.schemas.dataset import ValidationResult
from app.validators.raster_validator import RasterValidator

class PairValidator:
    def __init__(self):
        self.raster_validator = RasterValidator()

    def validate_bitemporal_pair(self, path_t1: str, path_t2: str) -> ValidationResult:
        """
        Validates two images to ensure they are compatible for Change Detection.
        Checks CRS matching, and alerts on dimension/modality mismatches.
        """
        res1 = self.raster_validator.validate_single_image(path_t1)
        res2 = self.raster_validator.validate_single_image(path_t2)
        
        combined_result = ValidationResult(valid=True)
        
        # Propagate upstream errors
        if not res1.valid or not res2.valid:
            combined_result.valid = False
            combined_result.errors.extend(res1.errors + res2.errors)
            return combined_result
            
        # Compatibility Checks
        if res1.crs != res2.crs:
            combined_result.valid = False
            combined_result.errors.append(f"CRS mismatch: {res1.crs} vs {res2.crs}")
            
        if res1.dimensions != res2.dimensions:
            combined_result.warnings.append("Dimensions mismatch. Images will require alignment/resampling.")
            
        if res1.detected_modality != res2.detected_modality:
            combined_result.warnings.append("Cross-modality pair detected (e.g. Optical/SAR). Ensure a fusion model is selected.")
            
        combined_result.metadata = {
            "image_1": res1.metadata,
            "image_2": res2.metadata
        }
        
        return combined_result
