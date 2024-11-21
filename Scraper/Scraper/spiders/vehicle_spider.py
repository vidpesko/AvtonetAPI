import scrapy
from scrapy.loader import ItemLoader

from Scraper.items import VehicleItem
from .translation_tables import CAR_BASIC_PROPERTY_DATA


class VehicleSpider(scrapy.Spider):
    name = "vehicle"

    allowed_domains = ["avto.net"]
    start_urls = [
        "https://www.avto.net/Ads/details.asp?id=20258324",
        # "https://www.avto.net/Ads/details.asp?id=20294615",
        # "https://www.avto.net/Ads/details.asp?id=20293150",
    ]

    def start_requests(self):
        # GET request
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={"use_nodriver": True},
            )

    def parse(self, response, **kwargs):
        # Initialise and set all attributes on Item object
        vehicle = ItemLoader(item=VehicleItem(), response=response)

        vehicle.add_value("url", response.url)
        raw_name_selector = response.css("h3")[0]
        vehicle.add_value("name", raw_name_selector.css("::text").get())
        vehicle.add_value("full_name", "".join(raw_name_selector.css("*::text").getall()))
        vehicle.add_css("price", ".h2::text")

        # Images
        vehicle.add_value("images", [img.xpath("@data-src").get() for img in response.xpath("//div[@id='lightgallery']/p")])
        vehicle.add_value("thumbnails", [
            img.xpath("@src").get()
            for img in response.xpath("//div[@class='GO-OglasThumb']/img")
        ])

        # Basic property table
        table_selector = respon(
            "//div[contains(., 'Prva registracija')]/ancestor::div[contains(@class, 'col-12')][1]"
        )[1]
        raw_properties = {property.css(".text-muted::text").get(): property.css("h5::text").get() for property in table_selector.css(".col-6")}
        # Enumerate translation table and use specified properties
        properties = {CAR_BASIC_PROPERTY_DATA.get(key, key):value for key, value in raw_properties.items()}

        print(properties)


        yield "vehicle"
