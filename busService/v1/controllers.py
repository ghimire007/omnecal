from userService.v1.models import User
from companyService.v1.models import Company
from busService.v1.models import Bus, Trip, BusLocation, BusTrackingHistory
from config.database import database
from typing import Dict
from sqlalchemy.sql.expression import exists, select, insert, update, delete
from config.config import AuthJWT


class BusController:
    async def create_bus(self, bus: Dict):
        query = insert(Bus).values(**bus)
        return await database.execute(query)

    @staticmethod
    async def check_bus_by_number(number: str) -> bool:
        query = select(Bus).where(Bus.bus_number == number)
        return await database.execute(select(exists(query)))

    @staticmethod
    async def get_bus_by_id(id: int) -> Bus:
        query = select(Bus).where(Bus.id == id)
        return await database.fetch_one(query)

    async def update_bus(self, id: int, data: Dict) -> Bus:
        query = update(Bus).values(data).where(Bus.id == id)
        return await database.execute(query)

    def create_bus_token(
        self, TokenHandler: AuthJWT, bus_id: int, bus_number: str
    ) -> str:
        return TokenHandler.create_access_token(
            subject=f"{bus_id}__{bus_number}", expires_time=5000 * 24 * 60 * 60
        )


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


class BusLocationController:
    async def create_bus_location(self, data: Dict):
        query = insert(BusLocation).values(**data)
        return await database.execute(query)

    async def check_bus_location(self, bus_id: int):
        query = select(BusLocation).where(BusLocation.bus == bus_id)
        return await database.execute(select(exists(query)))

    async def update_bus_location(self, data: Dict, bus_id: int):
        query = (
            update(BusLocation).values(data).where(BusLocation.bus == bus_id)
        )
        return await database.execute(query)

    async def delete_bus_location(self, bus_id: int):
        query = delete(BusLocation).where(BusLocation.bus == bus_id)
        return await database.execute(query)

    async def create_bus_history(self, data: Dict):
        query = insert(BusTrackingHistory).values(**data)
        return await database.execute(query)
