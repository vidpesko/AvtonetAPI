import scrapy.item
from urllib.parse import parse_qs, urlparse

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .items import Vehicle, Error


class ErrorPipeline:
    """
    Handle errors
    """
    
    def process_item(self, item: Error, spider):
        adapter = ItemAdapter(item)

        # if adapter.get("error_code"):

        return item


class VehiclePipeline:
    """
    Handle and process Vehicle item.
    Tasks:
        - add avtonet_id
        - store data to database
    """

    def process_item(self, item: Vehicle, spider):
        adapter = ItemAdapter(item)

        # Extract id
        if adapter.get("url"):
            parsed_url = urlparse(adapter.get("url"))
            avtonet_id = parse_qs(parsed_url.query)["id"][0]
            if avtonet_id:
                try:
                    adapter["avtonet_id"] = int(avtonet_id)
                except ValueError:
                    adapter["avtonet_id"] = avtonet_id

        return item


class ToDictPipeline:
    """
    Convert Item to JSON serializable
    """

    def process_item(self, item: scrapy.item, spider):
        return item.to_dict()