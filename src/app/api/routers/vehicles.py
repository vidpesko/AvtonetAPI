from typing import Annotated

from fastapi import APIRouter, Depends
from celery.result import AsyncResult

# from app.api.dependencies.auth import validate_is_authenticated

from app.api.dependencies.core import DBSessionDep
from app.api.dependencies.validation import validate_avtonet_vehicle_page_url
from app.crud.vehicle_operations import get_vehicle
from app.schemas.vehicle_schemas import ScrapeJobResponse, VehicleDataResponse
from app.scraper_interface import vehicle_scraper


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

    return ""
    # client = c.ScraperApiClient("amqp:://localhost/", "avtonet_api_queue")
    # client.connect()
    # return client.get(url)

    # job_id = vehicle_scraper.scrape_vehicle_page(url)
    # return ScrapeJobResponse(job_id=job_id, url=url)


@router.get("/job/{job_id}")
async def get(job_id):
    result = AsyncResult(job_id)

    match result.state:
        case "FAILURE":
            return VehicleDataResponse(job_status="error")
        case "SUCCESS":
            code = result.get()
            if code > 0:
                job_status = "error"
            else:
                job_status = "success"

            return VehicleDataResponse(job_status=job_status, job_output_code=code)
        case "PENDING":
            return VehicleDataResponse(job_status="processing")
