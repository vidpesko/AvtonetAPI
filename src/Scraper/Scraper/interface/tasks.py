import json, dataclasses
from celery import Celery
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings

from Scraper.items import Vehicle
from src.Scraper.Scraper.utils.formatting_utils import EnhancedJSONEncoder


app = Celery(
    "tasks",
    broker="amqp://testuser:testpassword@localhost:5672/testvhost",
    backend="redis://localhost:6379/0",
)


@app.task
def add(x, y):
    return x + y


@app.task
def get_vehicle(urls: list[str]) -> list[Vehicle]:
    """
    Fixture to run VehicleSpider and return all yielded items
    """

    results: list[Vehicle] = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    process = CrawlerProcess(get_project_settings())

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    process.crawl("vehicle", urls)
    process.start()  # the script will block here until the crawling is finished

    return dataclasses.asdict(results[0])
    return ["vehicle"]

# if __name__ == "__main__":
#     v = get_vehicle()
#     print(v)
