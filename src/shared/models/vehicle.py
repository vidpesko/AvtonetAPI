from typing import Optional, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy import BigInteger, String, Text, func, Table, DateTime, ForeignKey

from . import Base


# class Reflected(DeferredReflection):
#     __abstract__ = True


# class Vehicle(Reflected, Base):
#     __tablename__ = "vehicles"


class Vehicle(Base):
    __tablename__ = "vehicles"

    avtonet_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, nullable=False
    )
    url: Mapped[str] = mapped_column(unique=True, nullable=False)
    vehicle_name: Mapped[Optional[str]]
    vehicle_full_name: Mapped[Optional[str]]
    price: Mapped[Optional[int]]
    discount_price: Mapped[Optional[int]]
    price_verbose: Mapped[Optional[str]]
    first_registration: Mapped[Optional[str]]
    new_vehicle: Mapped[Optional[bool]]
    available: Mapped[bool] = mapped_column(default=True)
    mileage: Mapped[Optional[int]]
    num_of_owners: Mapped[Optional[int]]
    fuel_type: Mapped[Optional[str]]
    engine_power: Mapped[Optional[int]]
    comment: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    additional_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.seller_id"))
    archive_technical_data_url: Mapped[Optional[str]]
    published_on_avtonet: Mapped[DateTime] = mapped_column(DateTime)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    seller: Mapped["Seller"] = relationship(back_populates="vehicles")
    images: Mapped[List["VehicleImage"]] = relationship(back_populates="vehicle")

    def __str__(self):
        return f"Vehicle(avtonet_id={self.avtonet_id}, vehicle_name={self.vehicle_name}, url={self.url})"


class Seller(Base):
    __tablename__ = "sellers"

    seller_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    seller_type: Mapped[str]
    name: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    registered_from: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    address: Mapped[Optional[str]]
    opening_hours: Mapped[Optional[dict]] = mapped_column(JSONB)
    presentation: Mapped[Optional[str]]
    logo: Mapped[Optional[str]]
    tax_number: Mapped[Optional[str]]

    phone_numbers: Mapped[List["SellerPhoneNumber"]] = relationship(back_populates="seller")
    vehicles: Mapped[List["Vehicle"]] = relationship(back_populates="seller")

    def __str__(self):
        return f"Seller(seller_id={self.seller_id}, seller_type={self.seller_type})"


class SellerPhoneNumber(Base):
    __tablename__ = "sellers_phone_numbers"

    phone_number_id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.seller_id"))
    phone_number: Mapped[str]
    description: Mapped[Optional[str]]

    seller: Mapped["Seller"] = relationship(back_populates="phone_numbers")


class VehicleImage(Base):
    __tablename__ = "vehicle_images"

    image_id: Mapped[int] = mapped_column(primary_key=True)
    avtonet_url: Mapped[str]
    removed: Mapped[bool] = mapped_column(default=False)
    index: Mapped[int]
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.avtonet_id"))
    vehicle: Mapped["Vehicle"] = relationship(back_populates="images")

    def __str__(self):
        return f"{"X " if self.removed else ""}VehicleImage(image_id={self.image_id}, avtonet_url={self.avtonet_url}, vehicle_id={self.vehicle_id})"