from typing import Generator
from sqlalchemy.orm import Session
from config.database import SessionLocal
from typing import Callable


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_controller(
    repo_type: Callable,
):
    def _repo():
        return repo_type()

    return _repo
