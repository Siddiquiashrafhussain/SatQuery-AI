from abc import ABC, abstractmethod
from typing import Any, Dict
from app.schemas.tool_schema import ToolMetadata

class ISatQueryTool(ABC):
    """
    Abstract Base Class for all registered GIS Tools.
    Agents can ONLY execute tools that explicitly implement this interface.
    Arbitrary shell command execution by the agent is strictly prohibited by design.
    """
    
    @abstractmethod
    def get_metadata(self) -> ToolMetadata:
        """Returns the tool's signature and description for the Agent's Router."""
        pass
        
    @abstractmethod
    def execute(self, parameters: Dict[str, Any]) -> Any:
        """
        Executes the specific geospatial operation safely.
        Must contain strict input validation (e.g., path traversal checks) before execution.
        """
        pass
