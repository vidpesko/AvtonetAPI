import sys, os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Query, Depends, HTTPException
from sqlmodel import select
from celery.result import AsyncResult

from app.config import settings
from app.database import session_manager
from app.models.vehicle import Reflected
from app.api.routers import vehicles


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """

    # Execute on startup
    Reflected.prepare(session_manager._sync)

    yield

    # Execute on exit
    if session_manager._engine is not None:
        # Close the DB connection
        await session_manager.close()


app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/api/docs")


# Vehicle router: all operation regarding scraping vehicles
app.include_router(vehicles.router)


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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
