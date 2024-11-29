from pydantic import BaseModel


class ScrapeJobResponse(BaseModel):
    # When job is started, return data in this format
    job_id: str
    url: str


class VehicleDataResponse(BaseModel):
    # When job is finished, return vehicle data
    job_status: str
    job_output_code: int | None = None

    error: str | None = None