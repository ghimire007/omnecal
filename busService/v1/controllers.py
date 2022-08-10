from userService.v1.models import User
from companyService.v1.models import Company
from busService.v1.models import Bus, Trip, BusLocation
from busService.v1.models import BusRoute
from config.database import database
from typing import Dict
from sqlalchemy.sql.expression import exists, select, insert, update


class BusController:
    async def create_bus(self, bus: Dict):
        query = insert(Bus).values(**bus)
        return await database.execute(query)

    @staticmethod
    async def check_bus_by_number(number: str) -> bool:
        query = select(Bus).where(Bus.bus_number == number)
        return await database.execute(select(exists(query)))

    @staticmethod
    async def get_bus_by_id(number: id) -> Bus:
        query = select(Bus).where(Bus.id == id)
        return await database.fetch_one(query)


class TripController:
    async def create_trip(self, bus: Dict):
        query = insert(Trip).values(**bus)
        return await database.execute(query)

    async def create_tracking(self, tracking: Dict):
        query = insert(Trip).values(**tracking)
        return await database.execute(query)

    @staticmethod
    async def check_trip_by_id(number: str) -> bool:
        query = select(Trip).where(Trip.id == id)
        return await database.execute(select(exists(query)))

    @staticmethod
    async def get_trip_by_id(id: int) -> Trip:
        query = select(Trip).where(Trip.id == id)
        return await database.fetch_one(query)

    async def change_trip_status(self, id: int, status: str = "active") -> bool:
        query = update(Trip).values({"status": status}).where(Trip.id == id)
        return await database.execute(query)

    @staticmethod
    async def create_bus_route(data: Dict):
        query = insert(BusRoute).values(**data)
        return await database.execute(query)
