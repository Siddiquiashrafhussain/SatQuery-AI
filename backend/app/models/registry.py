from typing import Dict, List, Optional
from app.models.base import ISatQueryModel
from app.schemas.model_schema import ModelTask
from app.schemas.agent_schema import Modality

class ModelRegistry:
    """
    Central registry for all AI models. Allows the Agent Orchestrator to dynamically 
    discover and route tasks to the appropriate model based on capabilities.
    """
    def __init__(self):
        self._models: Dict[str, ISatQueryModel] = {}

    def register(self, model: ISatQueryModel) -> None:
        metadata = model.get_metadata()
        self._models[metadata.name] = model

    def get_model(self, name: str) -> Optional[ISatQueryModel]:
        return self._models.get(name)
        
    def list_models(self) -> List[dict]:
        return [model.get_metadata().model_dump() for model in self._models.values()]

    def find_models(self, task: ModelTask = None, modality: Modality = None) -> List[ISatQueryModel]:
        """Finds models matching specific requirements."""
        results = []
        for model in self._models.values():
            meta = model.get_metadata()
            if task and meta.task != task:
                continue
            if modality and modality not in meta.supported_modalities:
                continue
            results.append(model)
        return results

# Global singleton registry instance
model_registry = ModelRegistry()
