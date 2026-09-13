from app.agent.interfaces import IPlanner, IModelRouter, IToolRouter, IExecutor, IValidator, IEvidenceFusion, IConfidenceAssessment
from app.schemas.agent_schema import QueryContext, AnalysisPlan, ExecutionResult, Evidence, ConfidenceAssessment

class Orchestrator:
    def __init__(self, 
                 planner: IPlanner,
                 # The following will be injected when ML modules are ready
                 # model_router: IModelRouter,
                 # tool_router: IToolRouter,
                 # executor: IExecutor,
                 # validator: IValidator,
                 # fusion: IEvidenceFusion,
                 # assessor: IConfidenceAssessment
                 ):
        self.planner = planner
        # self.model_router = model_router
        # self.tool_router = tool_router
        # self.executor = executor
        # self.validator = validator
        # self.fusion = fusion
        # self.assessor = assessor

    def run(self, raw_query: str) -> dict:
        """
        Domain Logic (Layer 3)
        Manages the strict multi-step reasoning loop.
        """
        # 1. Query Understanding (Stubbed)
        context = QueryContext(
            original_query=raw_query,
            parsed_intent="STUB",
        )

        # 2. Planning
        plan: AnalysisPlan = self.planner.create_plan(context)
        
        # STUB: The rest of the chain
        # 3. Execution (which routes to models/tools)
        # results: List[ExecutionResult] = self.executor.execute_plan(plan, self.model_router, self.tool_router)
        
        # 4. Validation
        # is_valid = self.validator.validate_results(results, plan)
        
        # 5. Evidence Fusion
        # evidence: Evidence = self.fusion.fuse(results, context)
        
        # 6. Confidence Assessment
        # confidence: ConfidenceAssessment = self.assessor.assess(evidence, results)
        
        return {
            "query": raw_query,
            "plan_generated": plan.model_dump(),
            "status": "Awaiting downstream ML execution integrations."
        }
