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
    ARRAY,
    JSON,
)

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
        Column("token", String(350), unique=True, nullable=True),
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
        Column("longitude", DECIMAL(11, 8), nullable=False),
        Column("location", Geometry("POINT"), index=True, nullable=False),
        Column("speed", Float),
    )


class BusTrackingHistory(Base):
    __table__ = Table(
        "bus_tracking_history",
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
        ),
        Column("latitude", DECIMAL(10, 8), nullable=False),
        Column("longitude", DECIMAL(11, 8), nullable=False),
        Column("location", Geometry("POINT"), index=True, nullable=False),
        Column("speed", Float),
        Column("time", DateTime, server_default=func.now()),
    )


class Route(Base):
    __table__ = Table(
        "routes",
        metadata,
        Column(
            "id",
            BigInteger,
            primary_key=True,
            index=True,
            unique=True,
            nullable=False,
        ),
        Column("meta_data", JSON, nullable=False),
        Column("route", Geometry("LINESTRING"), nullable=False),
    )


class BusStops(Base):
    __table__ = Table(
        "bus_stops",
        metadata,
        Column(
            "id",
            BigInteger,
            primary_key=True,
            index=True,
            unique=True,
            nullable=False,
        ),
        Column("latitude", DECIMAL(10, 8), index=True, nullable=False),
        Column("longitude", DECIMAL(11, 8), index=True, nullable=False),
        Column("location", Geometry("POINT"), index=True, nullable=False),
        Column("name", String(250), nullable=False),
    )
