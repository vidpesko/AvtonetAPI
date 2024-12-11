import time
from typing import Annotated

from fastapi import APIRouter, Depends
from celery.result import AsyncResult

# from app.api.dependencies.auth import validate_is_authenticated

from app.api.dependencies.core import DBSessionDep
from app.api.dependencies.validation import validate_avtonet_vehicle_page_url
from app.crud.vehicle_operations import get_vehicle
from app.schemas.vehicle_schemas import ScrapeJobResponse, VehicleDataResponse
from app.scraper_interface import vehicle_page


router = APIRouter(
    prefix="/api/vehicle",
    tags=["vehicles"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/scrape",
    # response_model=ScrapeJobResponse,
    # dependencies=[Depends(validate_is_authenticated)],
)
async def scrape(
    url: Annotated[str, Depends(validate_avtonet_vehicle_page_url)],
    db_session: DBSessionDep,
):
    """
    Start scraping job
    """

    # output = run_spider("vehicle")
    # return output
    pass
    # return ScrapeJobResponse(job_id=job_id, url=url)
