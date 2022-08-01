from userService.v1.models import User
from companyService.v1.models import Company
from busService.v1.models import Bus
from config.database import database
from typing import Dict
from sqlalchemy.sql.expression import exists, select, insert


class BusController:
    async def create_bus(self, bus: Dict):
        query = insert(Bus).values(**bus)
        return await database.execute(query)

    @staticmethod
    async def check_bus_by_number(number: str) -> bool:
        query = select(Bus).where(Bus.bus_number == number)
        return await database.execute(select(exists(query)))
