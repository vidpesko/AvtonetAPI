"""
Tests for VehicleSpider defined in spiders/vehicle_spider.py
"""

import pytest
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher


@pytest.fixture
def response():
    """
    Fixture to run VehicleSpider and return all yielded items
    """

    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    process = CrawlerProcess(get_project_settings())

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    process.crawl("vehicle")
    process.start()  # the script will block here until the crawling is finished

    return results


@pytest.fixture
def response_single(response):
    """
    Return only the first item in response
    """

    return response[0]


def test_thumbnails_not_null(response_single):
    assert all(response_single["thumbnails"])
