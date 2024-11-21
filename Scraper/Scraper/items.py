from dataclasses import dataclass
from scrapy import Item

from .utils import cleanse_str


@dataclass
class VehicleItem(Item):
    """
    Base vehicle item, parent class for all types of vehicles.
    Defines all shared attributes
    """
    url: str | None = None
    name: str | None = None
    full_name: str | None = None
    avtonet_id: int | None = None
    # Price
    price: int | None = None
    price_verbose: str | None = None
    # Images
    images: list[str] = list
    thumbnails: list[str] = list
    # Basic propery table - the first one
    first_registration: str | None = None
    mileage: str | None = None
    num_of_owners: str | None = None
    fuel_type: str | None = None
    engine_power: str | None = None
