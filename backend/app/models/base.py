from abc import ABC, abstractmethod
from typing import Any
from app.schemas.model_schema import ModelMetadata

class ISatQueryModel(ABC):
    """
    Abstract Base Class that all ML models must implement.
    Named ISatQueryModel to avoid collision with Pydantic's BaseModel.
    """
    
    @abstractmethod
    def get_metadata(self) -> ModelMetadata:
        """Returns the model's static metadata."""
        pass
        
    @abstractmethod
    def load(self) -> None:
        """
        Loads the model weights into memory (CPU/GPU).
        MUST NOT be called automatically on startup.
        """
        pass
        
    @abstractmethod
    def predict(self, inputs: Any, **kwargs) -> Any:
        """Executes inference."""
        pass
