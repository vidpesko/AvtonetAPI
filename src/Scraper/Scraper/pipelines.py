import sys
from pathlib import Path

import scrapy.item

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .items import Vehicle, Error
from .utils.formatting_utils import cleanse_str
from .utils.parsing_utils import get_id_from_url


try:
    import shared
except ModuleNotFoundError:
    src_path = Path.cwd().parent.parent.absolute()
    sys.path.append(str(src_path))
finally:
    from shared.models import Vehicle as VehicleDB
    from shared.models import Seller as SellerDB
    from shared.models import VehicleImage as ImageDB
    from shared.config import settings


class ErrorPipeline:
    """
    Handle errors
    """
    
    def process_item(self, item: Error, spider):
        adapter = ItemAdapter(item)

        if adapter.get("error_message"):
            adapter["error_message"] = cleanse_str(adapter["error_message"])

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
        if adapter.get("url") and not adapter.get("error_code"):
            avtonet_id = get_id_from_url(adapter.get("url"))
            if avtonet_id:
                adapter["avtonet_id"] = avtonet_id

        # Save data
        engine = create_engine(settings.create_engine_url())
        with Session(engine) as session:
            item_dict = item.to_dict()
            del item_dict["images"]
            del item_dict["thumbnails"]
            del item_dict["seller_type"]

            # Save thumbnails
            # item_images = adapter.get("images")
            # item_thumbnails = adapter.get("thumbnails")
            # images = session.get()
            

            # Save seller
            # seller = session.get(SellerDB, adapter.get(""))

            vehicle = session.get(VehicleDB, adapter.get("avtonet_id"))

            if vehicle:
                for key, value in item_dict.items():
                    vehicle.__setattr__(key, value)
            else:
                vehicle = VehicleDB(
                    **item_dict
                )

                # Dummy seller
                seller = SellerDB(seller_type="person")
                seller.vehicles.append(vehicle)
                session.add(vehicle)

            session.commit()

        return item


class ToDictPipeline:
    """
    Convert Item to JSON serializable
    """

    def process_item(self, item: scrapy.item, spider):
        return item.to_dict()
