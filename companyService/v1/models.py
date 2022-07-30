"""from pkg_resources import require
from config.database import Base, metadata
import enum
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Table,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from userService.v1.models import Users

Company = Table(
        "Companies",
        metadata,
        Column("id", BigInteger, primary_key=True, index=True, unique=True),
        Column("name", String(50)),
        Column("address", String(100)),
        Column('owner',BigInteger, ForeignKey(Users.c.id,ondelete='CASCADE'), nullable=False),
        Column('document',String(200),nullable=True),
        Column("is_verfied", Boolean, default=False),
        Column("created_at", DateTime, default=func.now()),
    )

"""
