from pydantic import BaseModel
from typing import Dict

class Coordinate(BaseModel):
    lat: float
    lon: float

class FacilityTagWithCoordinate(Coordinate):
    facility_type: str

class Facility(BaseModel):
    facility: Coordinate