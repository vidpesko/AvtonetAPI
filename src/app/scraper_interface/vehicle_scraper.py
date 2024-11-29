import sys
sys.path.insert(0, "/Users/vidpesko/Documents/Learning/Projects/AvtonetAPI/src/app")

from urllib.parse import quote, urlparse, parse_qsl, urlencode, urlunparse

from app.config import settings
from scraper_interface.tasks import start_spider


def encode_url(url):
    # Parse the URL into components
    parsed_url = urlparse(url)

    # Parse the query parameters
    query_params = parse_qsl(parsed_url.query)

    # URL-encode the query parameters
    encoded_query = urlencode(query_params)

    # Reconstruct the URL with the encoded query
    encoded_url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            encoded_query,
            parsed_url.fragment,
        )
    )

    return encoded_url


def scrape_vehicle_page(url: str) -> str:
    """Wrapper for start_spider function, made specifically for vehicle page

    Args:
        url (str): vehicle page url
    Returns:
        str: job id
    """

    params = {"url": encode_url(url)}

    job = start_spider.delay(settings.vehicle_page_spider_name, params)

    return job.id
