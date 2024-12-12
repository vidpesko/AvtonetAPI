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


class CarInterface:
    def get_vehicle_page(self, url: str) -> dict:
        """Scrape vehicle listing page and return parsed data

        Args:
            url (str): url of that page

        Returns:
            dict: dict of vehicle data or error
        """

        parameters = {
            "url": url
        }

        response = run_spider(settings.car_listing_page_spider_name, parameters)[0]

        # Check for errors
        if response.get("exception", False):
            return response

        return response

    def get_listings_page(self):
        pass


class MotorcycleInterface:
    pass


if __name__ == "__main__":
    interface = CarInterface()
    response = interface.get_vehicle_page("https://www.avto.net/Ads/details.asp?ID=20178302")

    print(response)
