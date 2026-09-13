from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.schemas.agent_schema import Modality

class ValidationResult(BaseModel):
    valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    detected_modality: Optional[Modality] = None
    crs: Optional[str] = None
    dimensions: Optional[List[int]] = None # e.g., [width, height, bands]
