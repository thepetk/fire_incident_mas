from typing import Literal
from pydantic import BaseModel, Field


class FireEventSchema(BaseModel):
    """Output for Summarize Fire Report task."""

    location_x: float = Field(
        ..., description="Coordinate x of the fire event location."
    )
    location_y: float = Field(
        ..., description="Coordinate y of the fire event location."
    )
    fire_type: str = Field(
        ..., description="The type of the fire (ordinary, electrical, gas, etc.)"
    )
    injured_people: int = Field(..., description="Count of injured people.")
    fire_severity: Literal["low", "medium", "high"] = Field(
        ..., description="Count of injured people."
    )
