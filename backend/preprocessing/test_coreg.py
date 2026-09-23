import os
import rasterio
import numpy as np
from coregister import coregister_scenes
from shapely.geometry import box
import sys

def test_coreg():
    print("Testing Co-Registration...")
    
    # Create two dummy GeoTIFFs that overlap
    meta = {
        'driver': 'GTiff',
        'dtype': 'float32',
        'nodata': 0,
        'width': 100,
        'height': 100,
        'count': 1,
        'crs': 'EPSG:3857',
        'transform': rasterio.transform.from_origin(0, 1000, 10, 10)
    }
    
    os.makedirs("test_data", exist_ok=True)
    before_path = "test_data/before.tif"
    after_path = "test_data/after.tif"
    
    with rasterio.open(before_path, 'w', **meta) as dst:
        dst.write(np.ones((1, 100, 100), dtype=np.float32), 1)
        
    meta['transform'] = rasterio.transform.from_origin(500, 1500, 10, 10)
    with rasterio.open(after_path, 'w', **meta) as dst:
        dst.write(np.ones((1, 100, 100), dtype=np.float32) * 2, 1)
        
    output_before = "test_data/before_coreg.tif"
    output_after = "test_data/after_coreg.tif"
    
    try:
        coregister_scenes(before_path, after_path, output_before, output_after)
        print("Co-registration ran successfully without throwing exceptions.")
        
        with rasterio.open(output_before) as src_b, rasterio.open(output_after) as src_a:
            assert src_b.crs == src_a.crs, "CRSs do not match"
            assert src_b.shape == src_a.shape, f"Shapes do not match: {src_b.shape} != {src_a.shape}"
            assert src_b.transform == src_a.transform, "Transforms do not match"
            
            print("Verified: Outputs share identical CRS, pixel grid, and extent.")
    except Exception as e:
        print(f"FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_coreg()
