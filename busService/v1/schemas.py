from pydantic import BaseModel
from datetime import datetime
from typing import Optional, TypedDict, Any, Dict


class BusRegister(BaseModel):
    bus_number: str
    representative: Optional[int]


class TripRegister(BaseModel):
    driver: Optional[int]
    bus: int
    from_point: str
    to_point: str
    starts_at: datetime
    ends_at: datetime
    route: str


class BusLocation(BaseModel):
    latitude: float
    longitude: float
    speed: float


class Route(BaseModel):
    meta_data: dict
    towards_stop: list
    towards_destination: list
