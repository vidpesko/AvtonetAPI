import scrapy


class AwesomeSpider(scrapy.Spider):
    name = "awesome"

    def start_requests(self):
        # GET request
        yield scrapy.Request("https://httpbin.org/get", meta={"nodriver": True})

    def parse(self, response, **kwargs):
        # 'response' contains the page as seen by the browser
        return {"url": response.url}
