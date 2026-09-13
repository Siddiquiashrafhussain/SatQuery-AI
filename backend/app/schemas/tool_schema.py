from pydantic import BaseModel as PydanticBaseModel
from typing import List, Dict, Any

class ToolParameter(PydanticBaseModel):
    name: str
    type: str
    description: str
    required: bool = True

class ToolMetadata(PydanticBaseModel):
    name: str
    description: str
    category: str # e.g., "raster", "vector", "geometry", "projection"
    parameters: List[ToolParameter]
