import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.windows import from_bounds
from shapely.geometry import box

def coregister_scenes(before_path: str, after_path: str, output_before: str, output_after: str):
    """
    Co-registers two scenes by:
    1. Finding their intersection bounding box.
    2. Reprojecting both to a common CRS (EPSG:4326).
    3. Resampling to the finer resolution of the two.
    """
    with rasterio.open(before_path) as src_before, rasterio.open(after_path) as src_after:
        # Reproject both to 4326 for intersection calculation
        dst_crs = 'EPSG:4326'
        
        # Calculate transform and dimensions for reprojection of before scene
        transform_b, width_b, height_b = calculate_default_transform(
            src_before.crs, dst_crs, src_before.width, src_before.height, *src_before.bounds)
            
        transform_a, width_a, height_a = calculate_default_transform(
            src_after.crs, dst_crs, src_after.width, src_after.height, *src_after.bounds)
            
        # Find intersection in 4326
        # In rasterio, bounds are (left, bottom, right, top)
        bounds_b = rasterio.transform.array_bounds(height_b, width_b, transform_b)
        bounds_a = rasterio.transform.array_bounds(height_a, width_a, transform_a)
        
        poly_b = box(*bounds_b)
        poly_a = box(*bounds_a)
        
        intersection = poly_b.intersection(poly_a)
        if intersection.is_empty:
            raise ValueError("Scenes do not intersect.")
            
        # Target bounds
        target_bounds = intersection.bounds
        
        # Target resolution (use the finer one, smaller pixel size)
        res_b = (transform_b[0], -transform_b[4])
        res_a = (transform_a[0], -transform_a[4])
        target_res = (min(res_b[0], res_a[0]), min(res_b[1], res_a[1]))
        
        # Calculate target dimensions
        target_width = int((target_bounds[2] - target_bounds[0]) / target_res[0])
        target_height = int((target_bounds[3] - target_bounds[1]) / target_res[1])
        
        target_transform = rasterio.transform.from_origin(
            target_bounds[0], target_bounds[3], target_res[0], target_res[1]
        )
        
        kwargs = src_before.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': target_transform,
            'width': target_width,
            'height': target_height,
            'nodata': 0
        })
        
        # Write co-registered Before
        with rasterio.open(output_before, 'w', **kwargs) as dst:
            for i in range(1, src_before.count + 1):
                reproject(
                    source=rasterio.band(src_before, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src_before.transform,
                    src_crs=src_before.crs,
                    dst_transform=target_transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)
                    
        # Write co-registered After (use same kwargs, but update band count if needed)
        kwargs_a = src_after.meta.copy()
        kwargs_a.update({
            'crs': dst_crs,
            'transform': target_transform,
            'width': target_width,
            'height': target_height,
            'nodata': 0
        })
        
        with rasterio.open(output_after, 'w', **kwargs_a) as dst:
            for i in range(1, src_after.count + 1):
                reproject(
                    source=rasterio.band(src_after, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src_after.transform,
                    src_crs=src_after.crs,
                    dst_transform=target_transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)
