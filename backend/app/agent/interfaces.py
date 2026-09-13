from abc import ABC, abstractmethod
from typing import Any, List
from app.schemas.agent_schema import QueryContext, AnalysisPlan, ExecutionResult, Evidence, ConfidenceAssessment

class IQueryUnderstanding(ABC):
    @abstractmethod
    def parse_query(self, raw_query: str, image_metadata: dict) -> QueryContext:
        pass

class IPlanner(ABC):
    @abstractmethod
    def create_plan(self, context: QueryContext) -> AnalysisPlan:
        pass

class IModelRouter(ABC):
    @abstractmethod
    def route_to_model(self, model_name: str, inputs: Any) -> Any:
        pass

class IToolRouter(ABC):
    @abstractmethod
    def route_to_tool(self, tool_name: str, inputs: Any) -> Any:
        pass

class IExecutor(ABC):
    @abstractmethod
    def execute_plan(self, plan: AnalysisPlan, model_router: IModelRouter, tool_router: IToolRouter) -> List[ExecutionResult]:
        pass

class IValidator(ABC):
    @abstractmethod
    def validate_results(self, results: List[ExecutionResult], plan: AnalysisPlan) -> bool:
        pass

class IEvidenceFusion(ABC):
    @abstractmethod
    def fuse(self, results: List[ExecutionResult], context: QueryContext) -> Evidence:
        pass

class IConfidenceAssessment(ABC):
    @abstractmethod
    def assess(self, evidence: Evidence, results: List[ExecutionResult]) -> ConfidenceAssessment:
        pass
