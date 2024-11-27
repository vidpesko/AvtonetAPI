# from app.api.dependencies.auth import validate_is_authenticated
from app.api.dependencies.core import DBSessionDep
from app.crud.vehicle import get_vehicle
# from app.schemas.user import User
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{vehicle_id}",
    # response_model=User,
    # dependencies=[Depends(validate_is_authenticated)],
)
async def user_details(
    vehicle_id: int,
    db_session: DBSessionDep,
):
    """
    Get any user details
    """
    vehicle = await get_vehicle(db_session, vehicle_id)
    return vehicle
