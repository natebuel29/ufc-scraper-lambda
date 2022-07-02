from scrapy.crawler import CrawlerProcess
from scraper.spiders.future_fight_scraper import UfcFutureFightSpider

# issue resolved with this: https://aws.amazon.com/premiumsupport/knowledge-center/lambda-import-module-error-python/


def handler(event, context):
    process = CrawlerProcess()
    process.crawl(UfcFutureFightSpider)
    process.start()


if __name__ == "__main__":
    handler(None, None)
