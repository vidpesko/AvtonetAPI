from urllib.parse import parse_qs, urlparse

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .items import Vehicle
from .utils.item_utils import dataclass_to_json


class VehiclePipeline:
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

        return item.to_json()