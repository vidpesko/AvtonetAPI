import scrapy

from Scraper.items import Vehicle, VehicleLoader
from .translation_tables import CAR_BASIC_PROPERTY_DATA, CAR_METADATA_TABLE
from Scraper.utils import cleanse_str, str_to_int


class VehicleSpider(scrapy.Spider):
    name = "vehicle"

    allowed_domains = ["avto.net"]
    start_urls = [
        # "https://www.avto.net/Ads/details.asp?id=20258324",
        # "https://www.avto.net/Ads/details.asp?id=20294615",
        # "https://www.avto.net/Ads/details.asp?id=20293150",
        # "https://www.avto.net/Ads/details.asp?id=20305237&display=Audi%20A7"
        "https://www.avto.net/Ads/details.asp?id=20311825&display=Ssangyong%20Rexton"
    ]

    def __init__(self, start_urls = None, name = None, **kwargs):
        super().__init__(name, **kwargs)
        # Check if start_urls have been provided as argument to init
        if start_urls:
            self.start_urls = start_urls

    def start_requests(self):
        # GET request
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={"use_nodriver": True},
            )

    def parse(self, response, **kwargs):
        # Initialise and set all attributes on Item object
        vehicle = VehicleLoader(item=Vehicle(), response=response)

        vehicle.add_value("url", response.url)
        raw_name_selector = response.css("h3")[0]

        # Name
        vehicle.add_value("name", raw_name_selector.css("::text").get())
        vehicle.add_value("full_name", "".join(raw_name_selector.css("*::text").getall()))

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

        # Tables
        metadata = {}
        tables_selector = response.css("table")  # Select all tables
        # First table - "Osnovni podatki"
        first_table = tables_selector[0]  # "Osnovni podatki" table
        

        metadata["basic_data"] = first_table_data
        vehicle.add_value("metadata", metadata)

        # Seller type
        vehicle.add_css("seller_type", "#DealerAddress::text")

        # Images
        vehicle.add_value("images", [img.xpath("@data-src").get() for img in response.xpath("//div[@id='lightgallery']/p")])
        vehicle.add_value("thumbnails", [
            img.xpath("@src").get()
            for img in response.xpath("//div[@class='GO-OglasThumb']/img")
        ])

        yield vehicle.load_item()
