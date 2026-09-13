from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class Modality(str, Enum):
    OPTICAL = "optical"
    SAR = "sar"
    MULTISPECTRAL = "multispectral"
    FUSED = "fused"

class TemporalMode(str, Enum):
    SINGLE = "single"
    BI_TEMPORAL = "bi_temporal"
    TIME_SERIES = "time_series"

class AnalysisPlan(BaseModel):
    task: str = Field(..., description="High-level description of the analysis task")
    modality: Modality
    temporal_mode: TemporalMode
    required_models: List[str] = Field(default_factory=list)
    required_tools: List[str] = Field(default_factory=list)
    parameters: Dict[str, Any] = Field(default_factory=dict)

class QueryContext(BaseModel):
    original_query: str
    parsed_intent: str
    spatial_extent: Optional[Dict[str, Any]] = None
    time_range: Optional[Dict[str, Any]] = None

class ExecutionResult(BaseModel):
    step_name: str
    success: bool
    output: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Evidence(BaseModel):
    text_summary: str
    visual_artifacts: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)

class ConfidenceAssessment(BaseModel):
    overall_confidence: float
    factors: Dict[str, float]
    caveats: List[str]
