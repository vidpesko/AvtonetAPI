import datetime
from urllib.parse import urlparse
from urllib.parse import parse_qs

from app.config import Settings


def create_engine_url(settings: Settings, async_driver: bool=False) -> str:
    """Generate engine url using pydantic_settings class

    Args:
        settings (Settings): Settings class

    Returns:
        str
    """

    return f"postgresql{"+asyncpg" if async_driver else ""}://{settings.postgres_username}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}"


def extract_vehicle_id(url: str) -> int:
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    vehicle_id = params.get("id") if params.get("id") else params.get("ID", [0, ])

    return int(vehicle_id[0])


def get_time_difference(time_1: datetime.datetime, time_2: datetime.datetime = None) -> int:
    # Returns time difference in minutes
    if not time_2:
        time_2 = datetime.datetime.now()

    delta = time_2 - time_1
    difference = (delta.days * 24 * 60) + (delta.seconds / 60)
    return difference
