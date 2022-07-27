from userService.v1.models import Users
from fastapi import Depends
from config.database import database
from typing import Dict
from passlib.hash import bcrypt
from config.config import PASSWORD_HASH_ROUNDS
from sqlalchemy.sql.expression import exists, select
from config.config import AuthJWT
import re


class User:
    table = Users

    @classmethod
    async def create_user(cls, user: Dict):
        user["password"] = cls.hash_password(user["password"])
        query = cls.table.insert().values(**user)
        return await database.execute(query)

    @staticmethod
    def hash_password(password: str):
        return bcrypt.encrypt(password, rounds=PASSWORD_HASH_ROUNDS)

    @staticmethod
    def validate_password(password: str):
        pattern = re.compile(
            "^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])"
        )
        return re.match(pattern, password)

    @staticmethod
    def validate_mobile_number(number: str):
        return len(number) == 10 and number.isdigit()

    @classmethod
    async def create_user_tokens(cls, TokenHandler: AuthJWT, userid: int):
        return {
            "access_token": TokenHandler.create_access_token(subject=userid),
            "refresh_token": TokenHandler.create_refresh_token(subject=userid),
        }

    @classmethod
    async def create_access_token(cls, TokenHandler: AuthJWT, userid: int):
        return {
            "access_token": TokenHandler.create_access_token(subject=userid)
        }

    @classmethod
    async def check_user_by_phone(cls, number: str):
        query = cls.table.select().where(cls.table.c.mobile_number == number)
        query = select(exists(query))
        return await database.execute(query)

    @classmethod
    async def get_user_by_phone(cls, number: str):
        query = cls.table.select().where(cls.table.c.mobile_number == number)
        return await database.fetch_one(query)

    @classmethod
    async def authenticate_user(cls, mobile_number: str, password: str):
        user = await cls.get_user_by_phone(mobile_number)
        if not user:
            return False
        if not bcrypt.verify(password, user.password):
            return False
        return user
