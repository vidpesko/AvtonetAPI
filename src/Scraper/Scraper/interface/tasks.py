from importlib import import_module

from celery import Celery
from scrapy import signals
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from crochet import setup, wait_for


from ..spiders import vehicle_spider
from ..items import Vehicle


setup()  # Setuo crochet


app = Celery(
    "tasks",
    broker="amqp://testuser:testpassword@localhost:5672/testvhost",
    backend="redis://localhost:6379/0",
)

settings = get_project_settings()
crawler_runner = CrawlerRunner(settings)


@app.task
def get_vehicles(urls: list[str]) -> list[Vehicle]:
    """
    Run VehicleSpider asynchronously using Crochet.
    """
    results = []

    @wait_for(
        timeout=60.0
    )  # Crochet will block until the task is done or timeout occurs
    def run_crawl():
        """
        Run the Scrapy spider.
        """

        def collect_results(item, response, spider):
            """Collect items scraped by the spider."""
            print(item)
            results.append(item)

        # Connect the signals for item collection
        dispatcher.connect(collect_results, signal=signals.item_scraped)

        # Start the crawl
        return crawler_runner.crawl(vehicle_spider.VehicleSpider, start_urls=urls)

    # Start the crawl and wait for it to finish
    run_crawl()

    return results


# @wait_for(timeout=10.0)
# def run_spider(*args):
#     # scrapy_var = import_module(module_name)  # do some dynamic import of selected spider
#     # spiderObj = scrapy_var.mySpider()  # get mySpider-object from spider module
#     crawler = CrawlerRunner(get_project_settings())  # from Scrapy docs
#     crawler.crawl(
#         vehicle_spider.VehicleSpider,
#         ["https://www.avto.net/Ads/details.asp?id=20300923&display=Jaguar%20XF"],
#     )  # from Scrapy docs


# @app.task
# def get_vehicles(urls: list[str], spider="vehicles") -> list[Vehicle]:
#     """
#     Run VehicleSpider and return all yielded items
#     """

#     results: list[Vehicle] = []

#     # def crawler_results(signal, sender, item, response, spider):
#     #     results.append(item)

#     # process = CrawlerProcess(get_project_settings())

#     # dispatcher.connect(crawler_results, signal=signals.item_scraped)

#     # process.crawl("vehicle", urls)
#     # process.start(stop_after_crawl=True)  # the script will block here until the crawling is finished

#     run_spider(urls)

#     return results
