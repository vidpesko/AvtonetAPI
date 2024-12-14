import subprocess, time
from urllib.parse import quote, urlparse, parse_qsl, urlencode, urlunparse

from shared.config import settings


def generate_spider_params_string(params: dict) -> str:
    """Generates param string that can be passed to -a argument of scrapy crawl

    Args:
        params (dict): parameters

    Returns:
        str: parameter string
    """

    parameters = ""
    for key, value in params.items():
        value = str(value)
        # Check if spaces are present in value
        if value.find(" ") == -1:
            parameters += f"{key}={str(value)} "
        else:
            parameters += f"{key}='{str(value)}' "

    return parameters


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
    print(url, encoded_url)
    return encoded_url


def start_spider(spider_name: str, params: dict = None) -> int:
    """
    Runs run_spider.sh script. It starts scrapy spider and blocks until finished. After completion, it returns system exit code

    Args:
        spider_name (str): name of the spider to run
        params (dict): key-value pairs of scrapy spider parameters (scrapy crawl <spider_name> -a <params>)

    Returns:
        _type_: _description_
    """

    # Generate command
    if params:
        parameter_string = generate_spider_params_string(params)
        code = subprocess.call(
            ["./scraper_interface/run_spider.sh", spider_name, parameter_string],
        )
    else:
        code = subprocess.call(
            ["./scraper_interface/run_spider.sh", spider_name],
        )

    return code


def scrape_vehicle_page(url: str) -> str:
    """Run scrapy spider for provided url. Url should lead to vehicle page

    Args:
        url (str): vehicle page url
    Returns:
        str: job id
    """

    params = {"url": encode_url(url)}
    process = start_spider(settings.vehicle_page_spider_name, params)

    return "hello"
    # return job.id
