import datetime
from urllib.parse import urlparse
from urllib.parse import parse_qs

from shared.config import Settings


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
