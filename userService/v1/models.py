from email.policy import default
from enum import unique
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
    disable = 4


# metadata=MetaData()


"""

class Users(Base):
    __tablename__="Users"
    id=Column(BigInteger,primary_key=True,index=True,unique=True)
    first_name=Column(String(32))
    last_name=Column(String(32))
    mobile_number=Column(String(15))
    category=Column(Enum(UserCategory))
    password=Column(String(20))



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
    Column("is_driver", Boolean, default=False),
    Column("is_admin", Boolean, default=False),
    Column("created_at", DateTime, default=func.now()),
)
