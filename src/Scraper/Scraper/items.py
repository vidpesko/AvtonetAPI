import json
from dataclasses import dataclass, field
from scrapy import Item
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Identity, MapCompose, Compose, Join

from .utils.item_utils import (
    process_str,
    process_int,
    process_seller_type,
    take_last,
    EnhancedJSONEncoder,
)


@dataclass
class Vehicle:
    """
    Base vehicle item, parent class for all types of vehicles.
    Defines all shared attributes
    """
    url: str | None = field(default=None)
    name: str | None = field(default=None)
    full_name: str | None = field(default=None)
    avtonet_id: int | None = field(default=None)
    # Price
    price: int | None = field(default=None)
    discount_price: int | None = field(default=None)
    price_verbose: str | None = field(default=None)
    # Basic propery table - the first one
    first_registration: str | None = field(default=None)
    new_vehicle: bool | None = field(default=False)
    mileage: str | None = field(default=None)
    num_of_owners: str | None = field(default=None)
    fuel_type: str | None = field(default=None)
    engine_power: str | None = field(default=None)
    # Comment below property table
    comment: str | None = field(default=None)
    # Description
    description: str | None = field(default=None)
    # Inconsistent data / metadata
    metadata: dict = field(default_factory=dict)
    # Seller
    seller_type: str | None = field(default=None)
    # Images
    images: list[str] = field(default_factory=list)
    thumbnails: list[str] = field(default=list)


class VehicleLoader(ItemLoader):
    """
    Vehicle item loader class
    """
    default_input_processor = process_str()  # Default input proccessor: 1. cleanse all strings, 2. remove empty ones, 3. take first
    default_output_processor = TakeFirst()

    # Price
    price_in = process_int()  # 1. Cleanse str, 2. convert verbose price to number ("1.200 $" -> 1200)
    price_out = Compose(max)  # Choose highest price

    discount_price_in = price_in  # 1. Cleanse str, 2. convert verbose price to number ("1.200 $" -> 1200)

    # Basic property table
    # Vehicle age
    new_vehicle_in = process_str(
        lambda x: True if x == "NOVO VOZILO" else False
    )
    # Engine power
    engine_power_in = process_int()
    # Mileage
    mileage_in = process_int()
    # Owners
    num_of_owners = process_int()

    # Description
    description_in = Compose(
        Join(separator=""),
        str.strip
    )

    # Metadata
    metadata_in = Identity()
    metadata_out = take_last

    # Seller type
    seller_type_in = process_seller_type

    # Images
    images_in = Identity()
    images_out = Identity()
    thumbnails_in = Identity()
    thumbnails_out = Identity()