from pydantic import BaseModel as PydanticBaseModel, Field
from typing import List, Dict, Any
from enum import Enum
from app.schemas.agent_schema import Modality

class ModelTask(str, Enum):
    VQA = "vqa"
    GROUNDING = "grounding"
    CAPTIONING = "captioning"
    CHANGE_DETECTION = "change_detection"
    CHANGE_VQA = "change_vqa"
    OPTICAL_SAR = "optical_sar"

class ModelStatus(str, Enum):
    AVAILABLE = "available"
    LOADING = "loading"
    FAILED = "failed"
    OFFLINE = "offline"

class ModelMetadata(PydanticBaseModel):
    name: str
    version: str
    task: ModelTask
    supported_modalities: List[Modality]
    input_type: str
    output_type: str
    gpu_required: bool
    capabilities: List[str]
    status: ModelStatus = ModelStatus.OFFLINE
    parameters: Dict[str, Any] = Field(default_factory=dict)
