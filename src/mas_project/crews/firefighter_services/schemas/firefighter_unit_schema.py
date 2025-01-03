from pydantic import BaseModel, Field


class FirefighterUnitSchema(BaseModel):
    """Output for firefighter unit data"""

    uid: int = Field(..., description="The id of the unit.")
    location_x: float = Field(..., description="Coordinate x of the unit.")
    location_y: float = Field(..., description="Coordinate y of the unit.")
    unit_type: str = Field(
        ..., description="The type of the unit (truck, rescue, ladder etc.)"
    )
    personnel_capacity: int = Field(..., description="Capacity of firefighters.")
