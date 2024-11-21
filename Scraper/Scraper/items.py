from scrapy import Item, Field

from .utils import cleanse_str


class VehicleItem(Item):
    """
    Base vehicle item, parent class for all types of vehicles.
    Defines all shared attributes
    """
    url = Field()
    name = Field()
    full_name = Field()
    avtonet_id = Field()
    # Price
    price = Field()
    price_verbose = Field()
    # Images
    images = Field()
    thumbnails = Field()
