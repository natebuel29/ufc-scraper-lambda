from scrapy.crawler import CrawlerProcess
from scraper.spiders.future_fight_scraper import UfcFutureFightSpider


def handler(event, context):
    process = CrawlerProcess()
    process.crawl(UfcFutureFightSpider)
    process.start()


if __name__ == "__main__":
    handler(None, None)
