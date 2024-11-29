from app.config import settings
import sys
sys.path.insert(0, "/Users/vidpesko/Documents/Learning/Projects/AvtonetAPI/src/app")
from scraper_interface.tasks import start_spider


def scrape_vehicle_page(urls: list[str]) -> str:
    """Wrapper for start_spider function, made specifically for vehicle page

    Args:
        urls (list[str]): list of urls
    Returns:
        str: job id
    """

    params = {
        "urls": urls
    }

    job = start_spider.delay(settings.vehicle_page_spider_name, params)

    return job.id
