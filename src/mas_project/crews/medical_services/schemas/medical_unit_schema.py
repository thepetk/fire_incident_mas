from pydantic import BaseModel, Field


class MedicalUnitSchema(BaseModel):
    """Output for medical unit data"""

    uid: int = Field(..., description="The id of the unit.")
    location_x: int = Field(..., description="Coordinate x of the unit.")
    location_y: int = Field(..., description="Coordinate y of the unit.")
    available_beds: int = Field(
        ..., description="Number of available beds for the unit."
    )
