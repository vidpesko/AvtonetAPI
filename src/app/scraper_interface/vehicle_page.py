"""
Wrapper around Scraper/runner.py file, for interaction between FastAPI and scrapy
"""

try:
    from Scraper.Scraper.runner import run_spider
except ModuleNotFoundError:
    import sys
    import os
    src_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    sys.path.append(src_path)

    from Scraper.Scraper.runner import run_spider
from app.config import settings


def get_vehicle_page(url: str) -> dict:
    """Scrape vehicle listing page and return parsed data

    Args:
        url (str): url of that page

    Returns:
        dict: dict of vehicle data or error
    """

    parameters = {
        "url": url
    }

    response = run_spider(settings.vehicle_page_spider_name, parameters)

    return response


if __name__ == "__main__":
    response = get_vehicle_page("https://www.avto.net/Ads/details.asp?ID=20178302")

    print(response)
