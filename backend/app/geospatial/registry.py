from typing import Dict, List, Optional
from app.geospatial.base import ISatQueryTool

class ToolRegistry:
    """
    Central registry for all explicitly approved GIS tools.
    The agent can only interact with the system through tools registered here.
    """
    def __init__(self):
        self._tools: Dict[str, ISatQueryTool] = {}

    def register(self, tool: ISatQueryTool) -> None:
        metadata = tool.get_metadata()
        self._tools[metadata.name] = tool

    def get_tool(self, name: str) -> Optional[ISatQueryTool]:
        return self._tools.get(name)
        
    def list_tools(self) -> List[dict]:
        return [tool.get_metadata().model_dump() for tool in self._tools.values()]

# Global singleton registry instance
tool_registry = ToolRegistry()
