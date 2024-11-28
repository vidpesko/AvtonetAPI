from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Vehicle as VehicleDBModel


async def get_vehicle(db_session: AsyncSession, vehicle_id: int):
    vehicle = (
        await db_session.scalars(
            select(VehicleDBModel).where(VehicleDBModel.id == vehicle_id)
        )
    ).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="User not found")
    return vehicle


async def get_vehicle_by_url(db_session: AsyncSession, url: str):
    return (
        await db_session.scalars(
            select(VehicleDBModel).where(VehicleDBModel.url == url)
        )
    ).first()
