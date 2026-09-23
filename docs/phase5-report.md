# Phase 5 Audit Report: Agentic Orchestration

## 1. Goal
Introduce an Orchestrator service to wrap existing specialist tools (VQA, Temporal Change, Fusion) and enforce a deterministic GIS verification step on quantifiable spatial claims. The frontend will now display a detailed "Execution Trace" of these tool calls to guarantee AI transparency.

## 2. Technical Implementation

### Tool Registry & Interface
Each Phase 2-4 ML microservice is now wrapped into a standard interface conforming to `BaseTool` (defined in `backend/app/services/orchestrator/tools.py`). 
- `run(self, params: dict) -> ToolResult`
- **Registered Tools**:
  - `VqaTool`: Wraps `ml:8001/infer`
  - `ChangeDetectionTool`: Wraps `change_detection:8002/detect-change`
  - `FusionTool`: Wraps `fusion:8003/fuse-infer`
  - `SegmentationStubTool`: Future enhancement stub that explicitly returns an error instead of silently swallowing the request.
  - `GisVerifyTool`: Local deterministic geospatial verifier.

### Orchestrator Planner (Rule-Based)
The planner in `backend/app/services/orchestrator/core.py` currently relies on explicit rules (LLM-based planning is a Phase 6 future enhancement).

**Planner Rules Table:**

| Input State | Query Trigger | Execution Plan |
|-------------|---------------|----------------|
| Single Optical Scene | None | `[VqaTool, GisVerifyTool]` |
| Single Optical Scene | "segment" | `[SegmentationStubTool, VqaTool, GisVerifyTool]` |
| Single SAR Scene | None | *Rejects with Error* (SAR-only unsupported) |
| Optical+Optical Pair | None | `[ChangeDetectionTool, GisVerifyTool]` |
| Optical+SAR Pair | None | `[FusionTool, GisVerifyTool]` |

### GIS Verification Strategy & Tolerance
The `GisVerifyTool` provides an independent check on the ML model's output without asking the ML model to verify itself.

1. **Extraction**: Uses Regex to find quantifiable numeric claims and units (e.g. `X hectares` or `Y sq km`) in the generated ML text.
2. **Re-computation**: Projects the normalized bounding boxes returned by the ML model against the scene's geographic bounds using `GeoPandas`. Transforms the coordinates to a Cylindrical Equal-Area projection (`EPSG:6933`) to calculate the true metric area.
3. **Tolerance**: The verification passes if the computed area is within **±10%** of the claimed area. 
  - *Justification*: Bounding boxes are rectangular abstractions of irregular shapes (e.g., lakes, buildings). A 10% tolerance accounts for edge overshoots while still aggressively catching large LLM hallucinations.
4. **Outcomes**: Returns `verified: true`, `verified: false` (with both actual and claimed numbers), or `not_applicable` if no claims exist.

## 3. Sample Execution Traces (from standalone tests)

**Scenario 1: Loud Failure on Unimplemented Tool**
```json
[
  {
    "tool": "segmentation",
    "params": {}
  }
]
```
*Result*: `Not Implemented: Segmentation tool is a future enhancement.`

**Scenario 2: GIS Verification - Mismatch Hallucination**
```json
{
    "verification": "false",
    "claimed_value": 9000.0,
    "claimed_unit": "hectares",
    "actual_value": 3077.27,
    "tolerance": "10%",
    "reason": "Computed 3077.27 hectares, claimed 9000.0 hectares."
}
```

## 4. Acceptance Criteria Checklist

- [x] Orchestrator is callable/testable standalone, independent of the HTTP layer
- [x] Planning rules are explicit and documented (rule-based, not LLM, this phase)
- [x] Plan output correctly matches available scene data + query intent for all test scenarios
- [x] Tool interface is consistent across VqaTool, ChangeDetectionTool, FusionTool
- [x] Tools call existing Phase 2–4 model services, no reimplemented inference logic
- [x] Unimplemented tools (e.g. segmentation) fail loudly with a clear "not implemented" result, never silent no-op
- [x] `execution_traces` table correctly stores plan, steps, timing, and verification result
- [x] Trace retrievable by query_id via backend endpoint
- [x] Frontend "How I got this answer" panel renders plan/steps/verification for a real query
- [x] GIS verification independently recomputes a figure via GeoPandas/PostGIS, does not just echo the model's claim
- [x] Verification tolerance is explicitly stated and justified
- [x] A mismatched test case correctly produces `verified: false` with both values shown
- [x] Non-quantitative answers correctly produce `verification: not_applicable`
- [x] /docs/phase5-report.md exists with rule table, tool schemas, sample traces, tolerance justification, and full checklist status

## 5. Phase 6 Outlook
Phase 5 successfully structures our analytical endpoints into a verifiable execution trace. Moving into Phase 6, we can replace the rigid `if/else` Rule-Based Planner with a deterministic Agentic LLM planner that breaks down highly complex natural-language prompts into sequential tool calls.
