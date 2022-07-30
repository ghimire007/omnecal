from config.database import Base, metadata
import enum
from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Enum,
    Table,
    Boolean,
    DateTime,
    func,
)


class UserCategory(enum.Enum):
    student = 1
    regular = 2
    elder = 3
    disable = (4,)
    owner = (5,)
    driver = (6,)
    staff = (7,)
    superuser = 8


# metadata=MetaData()


class User(Base):
    __table__ = Table(
        "Users",
        metadata,
        Column("id", BigInteger, primary_key=True, index=True, unique=True),
        Column("first_name", String(32)),
        Column("last_name", String(32)),
        Column("mobile_number", String(15), unique=True, index=True),
        Column("category", Enum(UserCategory), index=True),
        Column("password", String(250)),
        Column("is_admin", Boolean, default=False),
        Column("is_admin", Boolean, default=True),
        Column("created_at", DateTime, default=func.now()),
    )


"""


Users = Table(
    "Users",
    metadata,
    Column("id", BigInteger, primary_key=True, index=True, unique=True),
    Column("first_name", String(32)),
    Column("last_name", String(32)),
    Column("mobile_number", String(15), unique=True, index=True),
    Column("category", Enum(UserCategory), index=True),
    Column("password", String(250)),
    Column("is_admin", Boolean, default=False),
    Column("is_admin", Boolean, default=True),
    Column("created_at", DateTime, default=func.now()),
)




"""
