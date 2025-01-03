from typing import List
from pydantic import BaseModel, Field


class MedicalUnitSchema(BaseModel):
    """Output for medical unit data"""

    uid: int = Field(..., description="The id of the unit.")
    location_x: float = Field(..., description="Coordinate x of the unit.")
    location_y: float = Field(..., description="Coordinate y of the unit.")
    available_beds: int = Field(
        ..., description="Number of available beds for the unit."
    )


class MedicalUnitListSchema(BaseModel):
    """Output for medical unit list data"""

    items: List[MedicalUnitSchema]
