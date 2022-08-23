from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from src.scraper.spiders.previous_event_scraper import UfcPreviousEventScraper
import logging


def handler(event, context):
    logging.getLogger().setLevel(logging.INFO)
    logging.info(
        f"Kicking off {context.function_name} with Lambda Request ID {context.aws_request_id}")
    configure_logging()
    settings = get_project_settings()  # settings not required if running
    runner = CrawlerRunner(settings)  # from script, defaults provided
    runner.crawl(UfcPreviousEventScraper)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
