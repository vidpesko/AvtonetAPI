from urllib.parse import parse_qs, urlparse

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .utils.utils import cleanse_str, str_to_int


class VehiclePipeline:
    def process_item(self, item, spider):
        return item
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
        # Cleanse name
        if adapter.get("name"):
            adapter["name"] = cleanse_str(adapter["name"])

        if adapter.get("full_name"):
            adapter["full_name"] = cleanse_str(adapter["full_name"])

        # Cleanse price and convert it to int
        if adapter.get("price"):
            price = cleanse_str(adapter["price"])
            try:
                adapter["price"] = str_to_int(price)
            except:
                adapter["price"] = 0

        return item
