from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models import Vehicle as VehicleDBModel


async def get_vehicle_from_db(db_session: AsyncSession, avtonet_id: int):
    vehicle = (
        await db_session.scalars(
            select(VehicleDBModel).where(VehicleDBModel.avtonet_id == avtonet_id)
        )
    ).first()
    # if not vehicle:
    #     raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


async def get_vehicle_by_url(db_session: AsyncSession, url: str):
    return (
        await db_session.scalars(
            select(VehicleDBModel).where(VehicleDBModel.url == url)
        )
    ).first()
