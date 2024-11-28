from typing import Annotated

from fastapi import APIRouter, Depends
from celery.result import AsyncResult

# from app.api.dependencies.auth import validate_is_authenticated

from app.api.dependencies.core import DBSessionDep
from app.api.dependencies.validation import validate_avtonet_urls
from app.crud.vehicle_operations import get_vehicle
from app.schemas.vehicle_schemas import ScrapeJobResponse, VehicleDataResponse

# from Scraper.interface import tasks  # type: ignore


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
    url: Annotated[list[str], Depends(validate_avtonet_urls)],
    db_session: DBSessionDep,
):
    """
    Start scraping job
    """


    # job = tasks.get_vehicles.delay(url)

    return ScrapeJobResponse(job_id="job.id", urls=url)


@router.get("/job/{job_id}")
async def get(job_id):
    result = AsyncResult(job_id)

    match result.state:
        case "FAILURE":
            return VehicleDataResponse(job_status="error")
        case "SUCCESS":
            data = result.get()
            return VehicleDataResponse(job_status="success", data=data)
        case "PENDING":
            return VehicleDataResponse(job_status="processing")
