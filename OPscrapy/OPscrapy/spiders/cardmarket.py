import scrapy


class CardmarketSpider(scrapy.Spider):
    name = "cardmarket"
    allowed_domains = ["cardmarket.com"]
    start_urls = ["https://cardmarket.com"]

    def parse(self, response):
        pass
