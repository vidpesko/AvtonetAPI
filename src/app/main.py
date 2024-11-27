import sys
sys.path.append("../Scraper")

from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, Depends, HTTPException
from sqlmodel import select
from celery.result import AsyncResult

from app.config import settings
from app.database import session_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """

    # Execute on startup
    yield

    # Execute on exit
    if session_manager._engine is not None:
        # Close the DB connection
        await session_manager.close()


app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/api/docs")




# @app.get("/vehicle")
# def root(urls: Annotated[list[str], Depends(validate_avtonet_urls)]):
#     # Check in db for vehicles. If found, check their updated_at propety


#     # Start celery process
#     task = get_vehicle.delay(urls)
#     # task = add.delay(1, 1)

#     return {"job_id": task.id}


# @app.get("/job/{job_id}")
# async def get(job_id):
#     result = AsyncResult(job_id)

#     match result.state:
#         case "FAILURE":
#             return {"error": True}
#         case "SUCCESS":
#             data = result.get()
#             return {"data": data}
#         case "PENDING":
#             return {"job_status": "processing"}
