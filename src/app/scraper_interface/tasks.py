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
def start_spider(spider_name: str, *args):
    """
    Run spider seperate from main proccess
    """

    # Generate command
    out = subprocess.run(
        ["./scraper_interface/run_spider.sh"],
        text=True,
        capture_output=True,
    )
