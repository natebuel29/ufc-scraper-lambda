import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from src.scraper.spiders.future_fight_scraper import UfcFutureFightSpider


def handler(event, context):
    configure_logging()
    settings = get_project_settings()  # settings not required if running
    runner = CrawlerRunner(settings)  # from script, defaults provided
    runner.crawl(UfcFutureFightSpider)  # your loop would go here
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
