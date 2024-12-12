from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from celery.result import AsyncResult

# from app.api.dependencies.auth import validate_is_authenticated

from app.api.dependencies.core import DBSessionDep
from app.api.dependencies.validation import validate_avtonet_vehicle_page_url
from app.crud.vehicle_operations import get_vehicle_from_db
from app.utils import get_time_difference
from app.config import settings
# from app.schemas.vehicle_schemas import ScrapeJobResponse, VehicleDataResponse
from app.scraper_interface import CarInterface


router = APIRouter(
    prefix="/api/car",
    tags=["vehicles", "car"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/listing",
    # response_model=list[dict],
    # dependencies=[Depends(validate_is_authenticated)],
)
async def scrape(
    url: Annotated[tuple, Depends(validate_avtonet_vehicle_page_url)],
    db_session: DBSessionDep,
    response: Response
):
    """
    Start scraping job
    """

    # 1. Check in db for vehicle instances
    url, vehicle_id = url

    if vehicle_id != 0:
        vehicle = await get_vehicle_from_db(db_session, vehicle_id)

        if vehicle:
            # Check for vehicle last update
            if get_time_difference(vehicle.updated_at) < settings.max_vehicle_age:
                return vehicle

    # 2. Scrape vehicle
    interface = CarInterface()
    scraping_response = interface.get_vehicle_page(url)

    if scraping_response.get("exception", False):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return scraping_response

    return scraping_response
