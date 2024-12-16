from ast import literal_eval

import scrapy, time

from ..items import Vehicle, VehicleLoader, Seller, SellerLoader, Error
from .translation_tables import CAR_BASIC_PROPERTY_DATA, CAR_METADATA_PARSING_TABLE, CAR_METADATA_VALUES_TABLE
from ..utils.parsing_utils import get_table_title


class VehicleSpider(scrapy.Spider):
    name = "vehicle"

    allowed_domains = ["avto.net"]
    start_urls = [
        # "https://www.avto.net/Ads/details.asp?id=20315148&display=Volkswagen%20Tiguan",
        # "https://www.avto.net/Ads/details.asp?id=20231532&display=Volkswagen%20Jetta",
        # "https://www.avto.net/Ads/details.asp?ID=20178302",
        "file:///Users/vidpesko/Documents/Learning/Projects/AvtonetAPI/src/Scraper/Scraper/spiders/site2.html",
        "file:///Users/vidpesko/Documents/Learning/Projects/AvtonetAPI/src/Scraper/Scraper/spiders/person.html"
    ]

    def __init__(self, start_urls = None, name = None, **kwargs):
        super().__init__(name, **kwargs)
        # Check if start_urls have been provided as argument to init

        if start_urls:
            self.start_urls = start_urls

        if kwargs.get("urls"):
            self.start_urls = literal_eval(kwargs["urls"])

        if kwargs.get("url"):
            self.start_urls = [kwargs["url"], ]

    # def start_requests(self):
    #     # GET request
    #     for url in self.start_urls:
    #         yield scrapy.Request(
    #             url,
    #             # meta={"use_scraperapi": True},
    #         )

    def parse(self, response, **kwargs):
        # Initialise and set all attributes on Item object
        vehicle = VehicleLoader(item=Vehicle(), response=response)
        seller = SellerLoader(item=Seller(), response=response)

        # Add URL & check availability
        is_error = "".join(response.css("h4 *::text").getall()).find("Napaka")
        if is_error != -1:
            # If error has occured (due to faulty link, expired offer,...)
            # Get error message
            error_msg = " ".join(response.css(".GO-Shadow-B *::text").getall())

            yield Error(url=response.url, error_code=404, description="Listing not found. Has it expired?", error_message=error_msg)
            return  # Exit to avoid running the rest of the code

        vehicle.add_value("url", response.url)

        # Name
        raw_name_selector = response.css("h3")[0]
        vehicle.add_value("vehicle_name", raw_name_selector.css("::text").get())
        vehicle.add_value("vehicle_full_name", "".join(raw_name_selector.css("*::text").getall()))

        # Price
        vehicle.add_css("price", ".h2 *::text")  # Regular price, without any modifiers (discounts,...)
        vehicle.add_xpath(
            "discount_price",
            "normalize-space(//p[contains(@class, 'GO-OglasDataStaraCena')]/following-sibling::p[1][contains(@class, 'h2')]/span/text())",
        )  # Discounted price

        # Basic property table
        basic_table_selector = response.xpath(
            "//div[contains(., 'Prevoženih')]/ancestor::div[contains(@class, 'col-12')][1]"
        )[1]
        raw_properties = {property.css(".text-muted::text").get(): property.css("h5::text").get() for property in basic_table_selector.css(".col-6")}
        # Enumerate translation table and use specified properties
        properties = {CAR_BASIC_PROPERTY_DATA.get(key, key):value for key, value in raw_properties.items()}
        for key, value in properties.items():
            try:
                vehicle.add_value(key, value)
            except KeyError:
                pass

        # Comment below basic property table
        try:
            comment_selector = basic_table_selector.css(".row")[1]
            vehicle.add_value("comment", comment_selector.css("*::text").getall())
        except IndexError:
            pass

        # Description
        vehicle.add_xpath("description", "//div[@id='StareOpombe']/node()")

        # Tables
        additional_data = {}
        tables_selector = response.xpath(
            "//div[contains(@class, 'col-12') and .//table[thead/tr/th[contains(text(), 'Osnovni podatki')]]]/table"
        )  # Select all tables
        # Enumerate all tables and add values to metadata dict
        for table in tables_selector:
            # Get table title
            table_title = get_table_title(table)
            # Check if table is defined in CAR_METADATA_PARSING_TABLE
            if table_title not in CAR_METADATA_PARSING_TABLE:
                continue
            table_handle_dict = CAR_METADATA_PARSING_TABLE[table_title]
            # Get and execute parsing function from CAR_METADATA_PARSING_TABLE
            parsing_func = table_handle_dict["parsing_function"]
            table_data = parsing_func(table, CAR_METADATA_VALUES_TABLE)

            new_table_title = table_handle_dict["new_table_title"]
            additional_data[new_table_title] = table_data

        vehicle.add_value("additional_data", additional_data)

        # Seller
        seller.add_css("seller_type", "#DealerAddress::text")  # Seller type

        seller_container = response.xpath("//div[normalize-space(text())='Prodajalec']/ancestor::div[contains(@class, 'container')]")[-1]

        # Logo
        try:
            logo = seller_container.css("img")[0]
            seller.add_value("logo", logo.xpath("@src").get())
        except IndexError:
            pass

        # Seller info - company
        try:
            seller_info_container = seller_container.css(
                ".border-info > .row > .d-lg-block"
            )[0]
            # Name
            name = seller_info_container.css("strong::text").get()
            # Location
            try:
                location = seller_info_container.xpath("//a[@data-target='#MapModal']")[0].css("*::text").getall()
            except IndexError:
                location = None
            # Phone numbers
            phone_container = seller_info_container.css(".list-unstyled li")
            seller.add_value(
                "phone_numbers",
                [
                    (
                        num.css("a::text").get(),  # Get actual phone number
                        num.xpath("./text()").getall(),  # Get phone title
                    )
                    for num in phone_container
                ],
            )
            # External website
            try:
                website = seller_info_container.xpath(
                    ".//i[contains(@class, 'fa-external-link')]/ancestor::div[contains(@class, 'row align-items-center')]"
                )[0].css("::text").getall()
                seller.add_value("website", website)
            except IndexError:
                website = None
            # Email
            try:
                email = seller_info_container.xpath(
                    ".//i[contains(@class, 'fa-envelope')]/ancestor::div[contains(@class, 'row align-items-center')]"
                )[0].css("::text").getall()
                # print(email)  # TODO: I get EMAIL PROTECTED???
            except IndexError:
                email = None
            # Opening hours
            try:
                hours_modal = response.css("#UrnikModal tr")
                opening_hours = [(hour.css("th::text").get(), hour.css("td::text").get()) for hour in hours_modal]
                seller.add_value("opening_hours", opening_hours)
            except IndexError:
                opening_hours = []
        except IndexError:
            # Seller info - person
            location = "few"
            name = "fex"
            email = "fex"

        seller.add_value("name", name)  # Name
        seller.add_value("address", location)
        # seller.add_value("email", email)
        # seller.add_value("email")
        vehicle.add_value("seller", seller.load_item())

        # Images
        vehicle.add_value("images", [img.xpath("@data-src").get() for img in response.xpath("//div[@id='lightgallery']/p")])
        vehicle.add_value("thumbnails", [
            img.xpath("@src").get()
            for img in response.xpath("//div[@class='GO-OglasThumb']/img")
        ])

        vehicle_item = vehicle.load_item()
        yield vehicle_item
