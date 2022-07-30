"""from userService.v1.models import Users
from companyService.v1.models import Company
from fastapi import Depends
from config.database import database
from typing import Dict
from sqlalchemy.sql.expression import exists, select


async def create_company(company:Dict):
    query = Company.insert().values(**company)
    return await database.execute(query)
"""
