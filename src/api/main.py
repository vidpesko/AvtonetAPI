import sys
sys.path.append("../Scraper")

from typing import Annotated
from urllib.parse import urlparse
from fastapi import FastAPI, Query, Depends, HTTPException
from celery.result import AsyncResult

from . import settings

from Scraper.interface.tasks import get_vehicle, add # type: ignore


# Dependencies
def validate_avtonet_urls(urls: list[str]) -> list[str]:
    for url in urls:
        # Parse url
        url_parse = urlparse(url)
        # Check scheme
        if url_parse.scheme not in settings.SCRAPER_ALLOWED_SCHEMES:
            raise HTTPException(
                status_code=400, detail="Wrong url. Invalid url schema"
            )
        # Check domain
        if url_parse.netloc not in settings.SCRAPER_ALLOWED_DOMAINS:
            raise HTTPException(
                status_code=400, detail="Wrong url. Invalid domain"
            )

    return q


app = FastAPI()


@app.get("/start")
def root(urls: Annotated[list[str], Depends(validate_avtonet_urls)]):
    # Start celery process
    task = get_vehicle.delay(urls)
    # task = add.delay(1, 1)

    return {"job_id": task.id}


@app.get("/get/{job_id}")
async def get(job_id):
    result = AsyncResult(job_id)

    match result.state:
        case "FAILURE":
            return {"error": True}
        case "SUCCESS":
            return {"data": result.get()}
        case "PENDING":
            return {"job_status": "processing"}
