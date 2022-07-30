from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import databases
from fastapi import FastAPI
from typing import Callable


def get_db() -> databases.Database:
    options = {
        "min_size": 2,
        "max_size": 10
        # "force_rollback": config.DB_FORCE_ROLL_BACK,
    }

    return databases.Database(DB_URL, **options)


DB_URL = f"postgresql://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('POSTGRES_HOST')}/{config('POSTGRES_DB')}"
Engine = create_engine(DB_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
database = get_db()
Base = declarative_base()
metadata = Base.metadata


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        print("connecting to a database")
        await database.connect()
        print("Database connection - successful")

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        print("connecting to a database")
        await database.disconnect()
        print("Database connection - successful")

    return stop_app
