from typing import Any

from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.utils.project import get_project_settings

# this is a class that will start the scrapper process
class ScrapperProcess:

    def __init__(self, crawler: Crawler):
        settings = get_project_settings()
        self.process = CrawlerProcess(settings)
        self.crawler = crawler

    def start(self, **args: Any):
        self.process.crawl(self.crawler, **args)
        self.process.start(stop_after_crawl=True, install_signal_handlers=True)

    def __del__(self):
        self.process.stop()
