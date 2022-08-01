from config.database import Base, metadata
import enum
from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Table,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.sql import expression
from userService.v1.models import User


class Company(Base):
    __table__ = Table(
        "Companies",
        metadata,
        Column("id", BigInteger, primary_key=True, index=True, unique=True),
        Column("name", String(100)),
        Column("address", String(100)),
        Column(
            "owner",
            BigInteger,
            ForeignKey("Users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column("document", String(250), nullable=True),
        Column("is_verfied", Boolean, default=False),
        Column("created_at", DateTime, default=func.now()),
    )


class Company_User(Base):
    __table__ = Table(
        "companyuser",
        metadata,
        Column("id", Integer, primary_key=True, index=True, unique=True),
        Column(
            "user",
            BigInteger,
            ForeignKey("Users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column(
            "company",
            BigInteger,
            ForeignKey("Companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column(
            "accepted",
            Boolean,
            server_default=expression.false(),
            nullable=False,
        ),
    )
