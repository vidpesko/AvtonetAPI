from urllib
from typing import Annotated

from fastapi import Query


def validate_avtonet_urls(urls: Annotated[list[str], Query()]) -> list[str]:
    for url in urls:
        # Parse url
        url_parse = urlparse(url)
        # Check scheme
        if url_parse.scheme not in settings.SCRAPER_ALLOWED_SCHEMES:
            raise HTTPException(status_code=400, detail="Wrong url. Invalid url schema")
        # Check domain
        if url_parse.netloc not in settings.SCRAPER_ALLOWED_DOMAINS:
            raise HTTPException(status_code=400, detail="Wrong url. Invalid domain")

    return urls
