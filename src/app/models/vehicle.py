from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy import BigInteger, String, Text, Integer, Boolean, JSON, TIMESTAMP, func, Table

from . import Base


# class Vehicle(Base):
#     __tablename__ = "vehicles"

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
#     vehicle_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
#     vehicle_full_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
#     price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
#     discount_price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
#     price_verbose: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
#     first_registration: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
#     new_vehicle: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
#     mileage: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
#     num_of_owners: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
#     fuel_type: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
#     engine_power: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
#     comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
#     description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
#     metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
#     seller_type: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

#     # Automatically managed timestamps
#     updated_at: Mapped[Optional[str]] = mapped_column(
#         TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True
#     )
#     created_at: Mapped[Optional[str]] = mapped_column(
#         TIMESTAMP, server_default=func.now(), nullable=True
#     )


class Reflected(DeferredReflection):
    __abstract__ = True


class Vehicle(Reflected, Base):
    __tablename__ = "vehicles"


# class VehicleImages(Base):
