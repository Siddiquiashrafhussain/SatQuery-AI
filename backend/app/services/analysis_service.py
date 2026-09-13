from app.agent.orchestrator import Orchestrator
from app.agent.planner import MockDevelopmentPlanner

class AnalysisService:
    def __init__(self):
        planner = MockDevelopmentPlanner()
        self.orchestrator = Orchestrator(planner=planner)

    def process_analysis_request(self, raw_query: str = "Analyze this image"):
        """
        Service (Layer 2)
        Handles business logic and delegates to the Agent domain logic.
        """
        # Business logic goes here (e.g., checking user quotas, logging request)
        
        # Delegate to orchestrator
        return self.orchestrator.run(raw_query)
