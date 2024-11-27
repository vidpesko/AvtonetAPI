from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy import BigInteger, String, Text, Integer, Boolean, JSON, TIMESTAMP, func, Table

from . import Base


class Reflected(DeferredReflection):
    __abstract__ = True


class Vehicle(Reflected, Base):
    __tablename__ = "vehicles"


# class VehicleImages(Base):
