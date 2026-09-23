import os
import sys

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.domain import Base, Scene, ScenePair
from app.services.orchestrator.core import Orchestrator
from app.core.config import settings
import json

def run_tests():
    engine = create_engine(settings.DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    
    orchestrator = Orchestrator(db)
    
    print("--- Test 1: Loud Failure on Segmentation ---")
    try:
        # We don't actually need a real scene in the DB if we mock the Scene object
        # but Orchestrator.execute() pulls from DB. Let's just create a mock scene
        # and test `generate_plan` and `execute` directly by mocking `db.query` or just inserting a test scene.
        
        from geoalchemy2.elements import WKTElement
        test_scene = Scene(
            id=9999,
            user_id=1,
            filename="test_opt.tif",
            storage_path="test_opt.tif",
            sensor_type="optical",
            bounds=WKTElement("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", srid=4326),
            crs="EPSG:4326"
        )
        
        plan = orchestrator.generate_plan(test_scene, None, "segment this area")
        print("Generated Plan:", json.dumps(plan, indent=2))
        assert plan[0]["tool"] == "segmentation"
        
        # Test execution of segmentation tool directly
        tool = orchestrator.tool_registry["segmentation"]
        res = tool.run({})
        print("Segmentation Stub Result:", res.error)
        assert res.error is not None
        print("Test 1 Passed.")
        
    except Exception as e:
        print("Test 1 Failed:", e)

    print("\n--- Test 2: GIS Verification Logic ---")
    try:
        verify_tool = orchestrator.tool_registry["gis_verify"]
        
        # Scenario A: Quantifiable claim, matching area
        # Scene is 1x1 degree near equator ~ 111km x 111km = 12,321 sq km
        # Let's say bounds is 0,0 to 0.1, 0.1 -> ~11km x 11km = 121 sq km = 12100 hectares
        scene_bounds = [0.0, 0.0, 0.1, 0.1]
        
        # Bbox covers exactly half the scene width and height = 0.25 area = ~3025 hectares
        res_a = verify_tool.run({
            "answer_text": "There are exactly 3000 hectares of forest.",
            "bounding_boxes": [[0.0, 0.0, 0.5, 0.5]],
            "scene_bounds": scene_bounds
        })
        print("Scenario A (Match):", res_a.output_data)
        assert res_a.output_data["verification"] == "true"
        
        # Scenario B: Quantifiable claim, mismatching area
        res_b = verify_tool.run({
            "answer_text": "I found 9000 hectares of water here.",
            "bounding_boxes": [[0.0, 0.0, 0.5, 0.5]],
            "scene_bounds": scene_bounds
        })
        print("Scenario B (Mismatch):", res_b.output_data)
        assert res_b.output_data["verification"] == "false"
        assert res_b.output_data["claimed_value"] == 9000
        
        # Scenario C: Non-quantitative
        res_c = verify_tool.run({
            "answer_text": "This is a beautiful dense forest.",
            "bounding_boxes": [[0.0, 0.0, 0.5, 0.5]],
            "scene_bounds": scene_bounds
        })
        print("Scenario C (Not Applicable):", res_c.output_data)
        assert res_c.output_data["verification"] == "not_applicable"
        
        print("Test 2 Passed.")
    except Exception as e:
        print("Test 2 Failed:", e)

if __name__ == "__main__":
    run_tests()
