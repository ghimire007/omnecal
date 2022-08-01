from config.database import Base, metadata
import enum
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Table,
    DateTime,
    func,
    ForeignKey,
)
from userService.v1.models import User
from companyService.v1.models import Company


class Bus(Base):
    __table__ = Table(
        "Bus",
        metadata,
        Column(
            "id",
            BigInteger,
            primary_key=True,
            index=True,
            unique=True,
            nullable=False,
        ),
        Column("bus_number", String(32), unique=True, nullable=False),
        Column(
            "owner",
            BigInteger,
            ForeignKey("Users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column(
            "representative",
            BigInteger,
            ForeignKey("Users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        Column(
            "company",
            BigInteger,
            ForeignKey("Companies.id", ondelete="SET NULL"),
            nullable=False,
        ),
        Column("document", String(200), nullable=True),
        Column("registered_at", DateTime, server_default=func.now()),
    )
