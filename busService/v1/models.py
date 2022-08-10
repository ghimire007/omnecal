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
    Enum,
    Integer,
    DECIMAL,
    Float,
)
from userService.v1.models import User
from companyService.v1.models import Company
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import ARRAY


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


class TripStatus(enum.Enum):
    inactive = 1
    active = 2
    onhold = 3
    terminated = 4
    completed = 5


class Trip(Base):
    __table__ = Table(
        "Trip",
        metadata,
        Column(
            "id",
            BigInteger,
            primary_key=True,
            index=True,
            unique=True,
            nullable=False,
        ),
        Column(
            "driver",
            BigInteger,
            ForeignKey("Users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column(
            "bus",
            BigInteger,
            ForeignKey("Bus.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column(
            "starts_at", DateTime, server_default=func.now(), nullable=False
        ),
        Column("ends_at", DateTime, nullable=False),
        Column("from_point", String(60), nullable=False, index=True),
        Column("to_point", String(60), nullable=False, index=True),
        Column("route", String(250), nullable=False, index=True),
        Column(
            "status",
            Enum(TripStatus),
            nullable=False,
            server_default="inactive",
        ),
    )


## first filter by criteria then show location


class BusLocation(Base):
    __table__ = Table(
        "buslocation",
        metadata,
        Column(
            "id",
            BigInteger,
            primary_key=True,
            index=True,
            unique=True,
            nullable=False,
        ),
        Column(
            "bus",
            BigInteger,
            ForeignKey("Bus.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        Column("latitude", DECIMAL(10, 8), nullable=False),
        Column("latitude", DECIMAL(11, 8), nullable=False),
        Column("location", Geometry("POINT"), index=True, nullable=False),
    )


class BusRoute(Base):
    __table__ = Table(
        "busroute",
        metadata,
        Column(
            "id",
            BigInteger,
            primary_key=True,
            index=True,
            unique=True,
            nullable=False,
        ),
        Column("latitude", DECIMAL(10, 8), nullable=False),
        Column("longitude", DECIMAL(11, 8), nullable=False),
        Column("bus_id", Integer, nullable=False),
        Column("address", String, nullable=False),
        Column("time", DateTime, server_default=func.now()),
    )
