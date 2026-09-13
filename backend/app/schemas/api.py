from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class HealthResponse(BaseModel):
    status: str
    version: str

class AnalysisRequest(BaseModel):
    query: str
    dataset_ids: List[str]
    options: Dict[str, Any] = Field(default_factory=dict)

class AnalysisResponse(BaseModel):
    job_id: str
    status: str
    message: str

class ConfidenceScore(BaseModel):
    score: float
    reasoning: str

class AnalysisResult(BaseModel):
    job_id: str
    status: str
    answer: Optional[str] = None
    confidence: Optional[ConfidenceScore] = None
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    spatial_outputs: List[Dict[str, Any]] = Field(default_factory=list)
    execution_trace: List[str] = Field(default_factory=list)
