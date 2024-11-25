import sys
sys.path.append("../Scraper")


from fastapi import FastAPI
from celery.result import AsyncResult

from Scraper.interface.tasks import get_vehicle, add # type: ignore

app = FastAPI()


@app.get("/start")
def root():
    # Start celery process
    task = get_vehicle.delay(
        ["https://www.avto.net/Ads/details.asp?id=20305237&display=Audi%20A7"]
    )
    # task = add.delay(1, 1)

    return {"job_id": task.id}


@app.get("/get/{job_id}")
async def get(job_id):
    result = AsyncResult(job_id)

    match result.state:
        case "FAILURE":
            return {"error": True}
        case "SUCCESS":
            print(result.get())
            return {"data": result.get()}
        case "PENDING":
            return {"job_status": "processing"}
