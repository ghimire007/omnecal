from userService.v1.models import User
from companyService.v1.models import Company, Company_User
from fastapi import Depends
from config.database import database
from typing import Dict
from sqlalchemy.sql.expression import exists, select, insert, update, and_


class CompanyController:
    async def create_company(self, company: Dict) -> int:
        query = insert(Company).values(**company)
        return await database.execute(query)

    async def invite_representative(self, company: int, user: int):
        query = insert(Company_User).values(company=company, user=user)
        return await database.execute(query)

    async def get_invite(self, company: int, user: int):
        query = select(Company_User).where(
            and_(Company_User.company == company, Company_User.user == user)
        )
        return await database.fetch_one(query)

    async def accept_invite(self, company: int, user: int):
        query = (
            update(Company_User)
            .values({"accepted": True})
            .where(
                and_(Company_User.company == company, Company_User.user == user)
            )
        )
        return await database.execute(query)

    @staticmethod
    async def check_invite(company: int, user: int):
        query = select(Company_User).where(
            and_(
                Company_User.company == company,
                Company_User.user == user,
                Company_User.accepted == False,
            )
        )
        query = select(exists(query))
        return await database.execute(query)

    @staticmethod
    async def check_related(company: int, user: int):
        query = select(Company_User).where(
            and_(
                Company_User.company == company,
                Company_User.user == user,
                Company_User.accepted == True,
            )
        )
        query = select(exists(query))
        return await database.execute(query)

    @staticmethod
    async def get_company_by_id(id: int) -> Company:
        query = select(Company).where(Company.id == id)
        return await database.fetch_one(query)

    @staticmethod
    async def check_company_by_id(id: int) -> bool:
        query = select(Company).where(Company.id == id)
        return await database.execute(select(exists(query)))
