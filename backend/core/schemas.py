from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class QueryRequest(BaseModel):
    """
    Standardized typed API contract for incoming query requests.
    """
    query: str = Field(..., description="The natural language or structured search query.")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional spatial or metadata filters.")
    dataset_id: Optional[str] = Field(None, description="The specific dataset to query against.")

class QueryResponse(BaseModel):
    """
    Standardized typed API contract for successful query responses.
    """
    job_id: str
    status: str = "processing"
    message: str = "Query has been submitted to the queue."
