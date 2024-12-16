import re
import sys
from pathlib import Path
from datetime import datetime

import scrapy.item

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from sqlalchemy import create_engine, select, insert, update
from sqlalchemy.orm import Session

from .items import Vehicle, Error, Seller
from .utils.formatting_utils import cleanse_str
from .utils.parsing_utils import get_id_from_url, str_to_date, encode_time


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


class SellerPipeline:
    def process_item(self, item: Vehicle | Error, spider):
        # If error, stop processing 
        if isinstance(item, Error):
            return item

        seller_item = item.seller
        adapter = ItemAdapter(seller_item)

        # Parse registered_from
        registered_from = adapter.get("registered_from")
        if registered_from:
            adapter["registered_from"] = str_to_date(registered_from, from_text=True)

        # Parse tax_number
        tax_number: str = adapter.get("tax_number")
        if tax_number:
            adapter["tax_number"] = tax_number.replace("DŠ:", "")

        # Parse opening hours -> [{"day": , "open_from": , "open_to": }]
        opening_hours_raw: list[list[str, str]] = adapter.get("opening_hours")
        opening_hours = []
        for day, value in opening_hours_raw:
            try:
                if value == "ZAPRTO":
                    _from = _to = 0
                else:
                    _from, _to = [encode_time(time) for time in re.findall(r"\b\d{1,2}:\d{2}\b", value)]
            except ValueError:
                _from = _to = value
            opening_hours.append({
                "day": day,
                "open_from": _from,
                "open_to": _to
            })
        adapter["opening_hours"] = opening_hours

        # Parse / reformat phone number -> [{"phone_number": , "description": }]
        phone_numbers_raw: list[list[str, str]] = adapter.get("phone_numbers")
        phone_numbers = []
        for num, description in phone_numbers_raw:
            phone_numbers.append({"phone_number": num, "description": description})
        adapter["phone_numbers"] = phone_numbers

        return item


class VehiclePipeline:
    """
    Handle and process Vehicle item.

    Tasks:
        - add avtonet_id
        - process & normalize data
        - store data to database
    """

    def process_item(self, item: Vehicle | Error, spider):
        adapter = ItemAdapter(item)
        engine = create_engine(settings.create_engine_url())

        # Extract id
        avtonet_id = 0
        # if adapter.get("url"):
        #     avtonet_id = get_id_from_url(adapter.get("url"))
        #     if avtonet_id:
        #         adapter["avtonet_id"] = avtonet_id

        # If error has occured (e.g. vehicle is no longer available), set available to false in db
        if isinstance(item, Error):
            with Session(engine) as session:
                vehicle = session.get(VehicleDB, avtonet_id)

                # If vehicle does not exist
                if not vehicle:
                    session.add(VehicleDB(avtonet_id=avtonet_id, url=adapter.get("url"), available=False))
                else:
                    vehicle.available = False

        # Normalize data
        # Parse first_registration. 2007 / 9 -> datetime
        first_registration: str = adapter.get("first_registration")
        if first_registration:
            try:
                year, month = first_registration.split(" / ")
                first_registration = datetime(int(year), int(month), 1)
            except ValueError:
                pass
            adapter["first_registration"] = first_registration

        # Parse published_on_avtonet_at
        published_on_avtonet_at = adapter.get("published_on_avtonet_at")
        if published_on_avtonet_at:
            adapter["published_on_avtonet_at"] = str_to_date(published_on_avtonet_at, from_text=True, include_time=True)

        # Save data
        # with Session(engine) as session:
        #     item_dict = item.to_dict()
        #     del item_dict["images"]
        #     del item_dict["thumbnails"]
        #     del item_dict["seller_type"]

        #     # Save thumbnails
        #     # item_images = adapter.get("images")
        #     # item_thumbnails = adapter.get("thumbnails")
        #     # images = session.get()

        #     # Save seller
        #     # seller = session.get(SellerDB, adapter.get(""))

        #     vehicle = session.get(VehicleDB, adapter.get("avtonet_id"))

        #     if vehicle:
        #         for key, value in item_dict.items():
        #             vehicle.__setattr__(key, value)
        #     else:
        #         vehicle = VehicleDB(
        #             **item_dict
        #         )

        #         # Dummy seller
        #         seller = SellerDB(seller_type="person")
        #         seller.vehicles.append(vehicle)
        #         session.add(vehicle)

        #     session.commit()

        return item


class ToDictPipeline:
    """
    Convert Item to JSON serializable
    """

    def process_item(self, item: scrapy.item, spider):
        return item.to_dict()
