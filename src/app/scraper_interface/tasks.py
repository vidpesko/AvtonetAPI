import subprocess

from celery import Celery

from app.config import settings


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
    subprocess.call(["scrapy", "crawl", spider_name])
