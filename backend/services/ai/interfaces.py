from abc import ABC, abstractmethod
from typing import Any, Dict

class AIModelInterface(ABC):
    """
    Base interface for all AI models in the system.
    Strictly enforces separation of API code and ML code.
    Allows hot-swapping models without rewriting endpoints.
    """
    
    @abstractmethod
    def load_model(self, model_path: str) -> None:
        """Loads the model artifacts into memory or GPU."""
        pass

    @abstractmethod
    def predict(self, input_data: Any, **kwargs) -> Dict[str, Any]:
        """
        Executes inference on the input data.
        Returns structured dictionary results.
        Do NOT hardcode results in implementations.
        """
        pass
