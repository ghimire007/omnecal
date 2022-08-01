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
from sqlalchemy.orm import relationship


class UserCat(enum.Enum):
    student = 1
    regular = 2
    elder = 3
    disable = 4
    owner = 5
    driver = 6
    staff = 7
    superuser = 8


# metadata=MetaData()


class User(Base):
    __table__ = Table(
        "Users",
        metadata,
        Column("id", BigInteger, primary_key=True, index=True, unique=True),
        Column("first_name", String(32), nullable=False),
        Column("last_name", String(32), nullable=False),
        Column(
            "mobile_number", String(15), unique=True, index=True, nullable=False
        ),
        Column("category", Enum(UserCat), index=True, nullable=False),
        Column("password", String(250), nullable=False),
        Column("is_admin", Boolean, default=False),
        Column("is_admin", Boolean, default=True),
        Column("created_at", DateTime, default=func.now()),
    )
    owned_companies = relationship("Company", backref="Owner", lazy="select")
    owned_buses = relationship(
        "Bus",
        backref="Owner",
        primaryjoin=("User.id==Bus.owner"),
        lazy="select",
    )
    companies = relationship("Company_User", backref="Staffs", lazy="select")

    buses = relationship(
        "Bus",
        backref="Staffs",
        primaryjoin=("User.id==Bus.representative"),
        lazy="select",
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
