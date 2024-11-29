import subprocess

from celery import Celery

try:
    from app.config import settings
except ModuleNotFoundError:
    from config import settings


app = Celery(
    "scraper_tasks",
    broker=settings.rabbitmq_broker_url,
    backend=settings.redis_backend_url,
)


@app.task
def start_spider(spider_name: str, params: dict=None):
    """
    Run spider seperate from main proccess
    """

    # Generate parameters
    parameters = ""
    for key, value in params.items():
        parameters += f"{key}={str(value)} "
    parameters = parameters.replace(" ", "")

    # Generate command
    code = subprocess.call(
        ["./scraper_interface/run_spider.sh", spider_name, parameters],
    )
    print(code)
