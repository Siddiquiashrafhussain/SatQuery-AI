import re
import logging
from typing import Dict, Any, Optional
import geopandas as gpd
from shapely.geometry import box
from app.services.orchestrator.tools import BaseTool, ToolResult

logger = logging.getLogger(__name__)

class GisVerifyTool:
    def run(self, params: dict) -> ToolResult:
        """
        Independent verification of spatial metrics.
        params expects:
        - answer_text: The generated answer from the ML model
        - bounding_boxes: List of bounding boxes [x1, y1, x2, y2] normalized 0-1
        - scene_bounds: Geographic bounds of the scene [min_lon, min_lat, max_lon, max_lat] in EPSG:4326
        """
        answer_text = params.get("answer_text", "")
        bboxes = params.get("bounding_boxes", [])
        scene_bounds = params.get("scene_bounds")
        
        if not scene_bounds:
            return ToolResult(
                output_data={"verification": "not_applicable", "reason": "No scene bounds provided."},
                raw_response={},
                error=None
            )
            
        # Regex to find quantifiable claims: e.g. "15 hectares" or "2 sq km"
        # Simplistic regex for the hackathon baseline: looks for a number followed by hectares/ha/sq km
        match = re.search(r'([\d\.]+)\s*(hectares|ha|sq km|square kilometers)', answer_text, re.IGNORECASE)
        
        if not match:
            return ToolResult(
                output_data={"verification": "not_applicable", "reason": "No quantifiable spatial claims found in answer."},
                raw_response={},
                error=None
            )
            
        claimed_value = float(match.group(1))
        unit = match.group(2).lower()
        
        # Calculate actual area if bboxes exist
        if not bboxes:
            return ToolResult(
                output_data={
                    "verification": "false", 
                    "claimed_value": claimed_value,
                    "claimed_unit": unit,
                    "actual_value": 0,
                    "reason": "Model claimed an area but provided no bounding boxes to verify."
                },
                raw_response={},
                error=None
            )
            
        min_lon, min_lat, max_lon, max_lat = scene_bounds
        scene_width = max_lon - min_lon
        scene_height = max_lat - min_lat
        
        polygons = []
        for b in bboxes:
            x1, y1, x2, y2 = b
            p_min_lon = min_lon + (x1 * scene_width)
            p_max_lat = max_lat - (y1 * scene_height)
            p_max_lon = min_lon + (x2 * scene_width)
            p_min_lat = max_lat - (y2 * scene_height)
            polygons.append(box(p_min_lon, p_min_lat, p_max_lon, p_max_lat))
            
        gdf = gpd.GeoDataFrame({'geometry': polygons}, crs="EPSG:4326")
        
        # Project to Equal-Area projection to calculate true area in sq meters.
        # EPSG:6933 (Cylindrical Equal Area) is commonly used globally for area calcs.
        gdf_ea = gdf.to_crs("EPSG:6933")
        
        total_area_sqm = gdf_ea.geometry.area.sum()
        
        if unit in ['hectares', 'ha']:
            computed_value = total_area_sqm / 10000.0
        elif unit in ['sq km', 'square kilometers']:
            computed_value = total_area_sqm / 1000000.0
        else:
            computed_value = total_area_sqm
            
        # Tolerance: +/- 10%
        tolerance = 0.10
        margin = claimed_value * tolerance
        
        is_verified = (computed_value >= (claimed_value - margin)) and (computed_value <= (claimed_value + margin))
        
        return ToolResult(
            output_data={
                "verification": "true" if is_verified else "false",
                "claimed_value": claimed_value,
                "claimed_unit": unit,
                "actual_value": round(computed_value, 2),
                "tolerance": "10%",
                "reason": f"Computed {computed_value:.2f} {unit}, claimed {claimed_value} {unit}."
            },
            raw_response={},
            error=None
        )

# Ensure it's exported
import sys
sys.modules[__name__].GisVerifyTool = GisVerifyTool
