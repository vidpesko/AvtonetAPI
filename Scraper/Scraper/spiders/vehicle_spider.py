import scrapy

from Scraper.items import VehicleItem


class AwesomeSpider(scrapy.Spider):
    name = "vehicle"
    start_urls = [
        "https://www.avto.net/Ads/details.asp?id=20258324",
        "https://www.avto.net/Ads/details.asp?id=20294615",
        "https://www.avto.net/Ads/details.asp?id=20293150",
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
        vehicle = VehicleItem()

        vehicle["url"] = response.url
        raw_name_selector = response.css("h3")[0]
        vehicle["name"] = raw_name_selector.css("::text").get()
        vehicle["full_name"] = "".join(raw_name_selector.css("*::text").getall())
        vehicle["price"] = response.css(".h2::text").get()

        vehicle["images"] = [img.xpath("@data-src").get() for img in response.xpath("//div[@id='lightgallery']/p")]
        vehicle["thumbnails"] = [
            img.xpath("@data-cookieblock-src").get()
            for img in response.xpath("//div[@class='GO-OglasThumb']/img")
        ]

        yield vehicle
