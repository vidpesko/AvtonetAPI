from pydantic import BaseModel


class ScrapeJobResponse(BaseModel):
    # When job is started, return data in this format
    job_id: str
    urls: list[str]


class VehicleDataResponse(BaseModel):
    # When job is finished, return vehicle data
    data: list[dict]