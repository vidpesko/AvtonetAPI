from urllib.parse import urlparse
from typing import Annotated

from fastapi import Query, HTTPException, Depends

from shared.config import settings
from app.utils import extract_vehicle_id


def validate_avtonet_url(url: Annotated[str, Query()]) -> str:
    # Parse url
    url_parse = urlparse(url)
    # Check scheme
    if url_parse.scheme not in settings.scraper_allowed_schemas:
        raise HTTPException(status_code=400, detail="Wrong url. Invalid url schema")
    # Check domain
    if url_parse.netloc not in settings.scraper_allowed_domains:
        raise HTTPException(status_code=400, detail="Wrong url. Invalid domain")

    return url


def validate_avtonet_vehicle_page_url(url: Annotated[str, Depends(validate_avtonet_url)]):
    # Check if url is for avto.net vehicle page -> it should start with "/Ads/details.asp". It also extracts vehicle id from it
    url_parse = urlparse(url)

    if url_parse.path != settings.vehicle_page_path_prefix:
        raise HTTPException(status_code=400, detail="Wrong url. It does not lead to avto.net vehicle detail page")

    # Extract vehicle id
    vehicle_id = extract_vehicle_id(url)

    return url, vehicle_id