from pydantic import BaseModel
from typing import Optional


class BusRegister(BaseModel):
    bus_number: str
    representative: Optional[int]
