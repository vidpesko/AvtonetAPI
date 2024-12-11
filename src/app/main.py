from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, Depends, HTTPException

from app.config import settings
from app.database import session_manager
from app.models.vehicle import Reflected
from app.api.routers import vehicles


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute on startup
    Reflected.prepare(session_manager._sync_engine)  # Reflect db using sync engine
    session_manager._sync_engine.dispose()  # Close that engine, it won't be needed

    yield

    # Execute on exit
    if session_manager._async_engine is not None:
        # Close the DB connection
        await session_manager.close()


app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/api/docs")


# Vehicle router: all operation regarding scraping vehicles
app.include_router(vehicles.router)
