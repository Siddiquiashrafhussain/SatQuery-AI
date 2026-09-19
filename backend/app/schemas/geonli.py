from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Any

class GeoNLIRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    premise: str = Field(min_length=1)
    hypothesis: str = Field(min_length=1)
    image_id: str | None = None

class GeoNLIResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    task: Literal["geonli"] = "geonli"
    entailment_class: Literal["entailment", "neutral", "contradiction"]
    reasoning: str
    premise: str
    hypothesis: str
    image_id: str | None = None
    provider: str
    model_name: str
