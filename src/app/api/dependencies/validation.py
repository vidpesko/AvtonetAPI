from urllib.parse import urlparse
from typing import Annotated

from fastapi import Query, HTTPException
from app.config import settings


def validate_avtonet_urls(url: Annotated[list[str], Query()]) -> list[str]:
    for u in url:
        # Parse url
        url_parse = urlparse(u)
        # Check scheme
        if url_parse.scheme not in settings.scraper_allowed_schemas:
            raise HTTPException(status_code=400, detail="Wrong url. Invalid url schema")
        # Check domain
        if url_parse.netloc not in settings.scraper_allowed_domains:
            raise HTTPException(status_code=400, detail="Wrong url. Invalid domain")

    return url
