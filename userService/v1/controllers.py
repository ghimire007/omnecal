from userService.v1.models import User
from fastapi import Depends
from config.database import database
from typing import Dict
from passlib.hash import bcrypt
from config.config import PASSWORD_HASH_ROUNDS
from sqlalchemy.sql.expression import exists, select, insert
from config.config import AuthJWT
import re


class UserController:
    async def create_user(self, user: Dict) -> int:
        user["password"] = self.hash_password(user["password"])
        query = insert(User).values(**user)
        return await database.execute(query)

    def hash_password(self, password: str) -> str:
        return bcrypt.encrypt(password, rounds=PASSWORD_HASH_ROUNDS)

    def validate_password(self, password: str):
        pattern = re.compile(
            "^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])"
        )
        return re.match(pattern, password)

    def validate_mobile_number(self, number: str) -> bool:
        return len(number) == 10 and number.isdigit()

    async def create_user_tokens(
        self, TokenHandler: AuthJWT, userid: int
    ) -> dict:
        return {
            "access_token": TokenHandler.create_access_token(subject=userid),
            "refresh_token": TokenHandler.create_refresh_token(subject=userid),
        }

    def create_access_token(self, TokenHandler: AuthJWT, userid: int) -> dict:
        return {
            "access_token": TokenHandler.create_access_token(subject=userid)
        }

    @staticmethod
    async def check_user_by_phone(number: str) -> bool:
        query = select(User).where(User.mobile_number == number)
        query = select(exists(query))
        return await database.execute(query)

    @staticmethod
    async def get_user_by_phone(number: str) -> User:
        query = select(User).where(User.mobile_number == number)
        return await database.fetch_one(query)

    @staticmethod
    async def get_user_by_id(id: int) -> User:
        query = select(User).where(User.id == id)
        return await database.fetch_one(query)

    @classmethod
    async def authenticate_user(
        cls, mobile_number: str, password: str
    ) -> bool | User:
        user = await cls.get_user_by_phone(mobile_number)
        if not user:
            return False
        if not bcrypt.verify(password, user.password):
            return False
        return user
