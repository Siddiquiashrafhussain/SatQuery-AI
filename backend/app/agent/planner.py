from app.agent.interfaces import IPlanner
from app.schemas.agent_schema import QueryContext, AnalysisPlan, Modality, TemporalMode

class MockDevelopmentPlanner(IPlanner):
    """
    DEV STUB: A deterministic mock planner for development.
    DO NOT USE IN PRODUCTION. Does not use LLMs.
    """
    def create_plan(self, context: QueryContext) -> AnalysisPlan:
        query = context.original_query.lower()
        
        # Simple deterministic mapping for development testing
        if "change" in query or "before and after" in query:
            return AnalysisPlan(
                task="Change Detection Analysis",
                modality=Modality.OPTICAL,
                temporal_mode=TemporalMode.BI_TEMPORAL,
                required_models=["ChangeDetectionModel_V1"],
                required_tools=["ImageAlignmentTool"],
                parameters={"threshold": 0.5}
            )
        elif "water" in query or "flood" in query:
            return AnalysisPlan(
                task="Water Body Extraction",
                modality=Modality.SAR, # Assuming SAR is best for flood
                temporal_mode=TemporalMode.SINGLE,
                required_models=["GroundingModel_SAR"],
                required_tools=["NDWI_Calculator", "MaskGenerator"],
                parameters={"water_index_threshold": 0.2}
            )
        else:
            return AnalysisPlan(
                task="General Visual QA",
                modality=Modality.OPTICAL,
                temporal_mode=TemporalMode.SINGLE,
                required_models=["VQA_Model_Base"],
                required_tools=[],
                parameters={}
            )
