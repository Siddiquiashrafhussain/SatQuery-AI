from app.models.base import ISatQueryModel
from app.schemas.model_schema import ModelMetadata, ModelTask, ModelStatus
from app.schemas.agent_schema import Modality
from typing import Any

class RemoteSensingVQAModel(ISatQueryModel):
    """
    STUB: Example implementation of a VQA Model.
    Used for architectural validation, does not download actual weights yet.
    """
    def __init__(self):
        self._metadata = ModelMetadata(
            name="RemoteSensingVQAModel",
            version="1.0.0",
            task=ModelTask.VQA,
            supported_modalities=[Modality.OPTICAL, Modality.MULTISPECTRAL],
            input_type="image_text_pair",
            output_type="text",
            gpu_required=True,
            capabilities=["vqa", "scene_classification", "counting"],
            status=ModelStatus.OFFLINE
        )
        self._is_loaded = False

    def get_metadata(self) -> ModelMetadata:
        return self._metadata

    def load(self) -> None:
        """Stubbed load method. Does NOT download large weights."""
        self._is_loaded = True
        self._metadata.status = ModelStatus.AVAILABLE
        # In the future:
        # self.model = AutoModelForCausalLM.from_pretrained(...)

    def predict(self, inputs: Any, **kwargs) -> Any:
        if not self._is_loaded:
            raise RuntimeError("Model is not loaded.")
        return {"answer": "STUB: Visual QA Answer", "confidence": 0.85}
