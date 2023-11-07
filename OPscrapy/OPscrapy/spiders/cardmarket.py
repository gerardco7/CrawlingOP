import scrapy

class CardmarketSpider(scrapy.Spider):
    name = "cardmarket"
    allowed_domains = ["cardmarket.com"]
    start_urls = ["https://www.cardmarket.com/en/OnePiece/Products/Singles?idCategory=1621&idExpansion=0&idRarity=0&sortBy=collectorsnumber_asc"]

    def parse(self, response):
        pass
