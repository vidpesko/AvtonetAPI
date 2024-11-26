from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import JSONB


class Vehicle(SQLModel, table=True):
    __tablename__ = "vehicle"

    id: int = Field(primary_key=True)
    url: str =  Field(unique=True)
    vehicle_name: str | None = Field(default=None)
    vehicle_full_name: str | None = Field(default=None)
    price: int | None = Field(default=None)
    discount_price: int | None = Field(default=None)
    price_verbose: str | None = Field(default=None)
    first_registration: str | None = Field(default=None)
    new_vehicle: bool | None = Field(default=None)
    mileage: int | None = Field(default=None)
    num_of_owners: int | None = Field(default=None)
    fuel_type: str | None = Field(default=None)
    engine_power: int | None = Field(default=None)
    comment: str | None = Field(default=None)
    description: str | None = Field(default=None)
    vehicle_metadata: dict | None = Field(
        default=None, sa_column=Column("metadata", JSONB)
    )
    seller_type: str | None = Field(default=None)
    last_updated: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)
