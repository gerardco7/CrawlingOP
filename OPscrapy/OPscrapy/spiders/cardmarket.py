import scrapy
from urllib.parse import urlencode
from scrapy.shell import inspect_response
from time import sleep

# TODO: conseguir imagen i link
# TODO: bug con precios de más de 1000€ con el punto

class CardmarketSpider(scrapy.Spider):
    name = "cardmarket"
    allowed_domains = ["85.215.9.83"]

    def start_requests(self):
        url = f"http://85.215.9.83/es/OnePiece/Products/Singles/"   
        yield scrapy.Request(url=url, callback=self.collections)

    def collections(self, response):
        self.collections= ["Awakening-of-the-New-Era", "Judge-Promos", "Kingdoms-of-Intrigue", "One-Piece-Products", "Paramount-War", "Pillars-of-Strength", "Premium-Bandai-Products", "Promos", "Promos-Kingdoms-of-Intrigue", "Promos-Paramount-War", "Promos-Pillars-of-Strength", "Reprints", "Romance-Dawn", "Special-Tournaments-Promos", "Starter-Deck-Absolute-Justice", "Starter-Deck-Animal-Kingdom-Pirates", "Starter-Deck-Big-Mom-Pirates", "Starter-Deck-MonkeyDLuffy", "Starter-Deck-ONE-PIECE-FILM-edition", "STARTER-DECK-Straw-Hat-Crew", "Starter-Deck-The-Seven-Warlords-of-the-Sea", "Starter-Deck-Worst-Generation", "Starter-Deck-Yamato", "Ultra-Deck-The-Three-Captains", "Unnumbered-Promos"]
        for collection in self.collections:
            url = f"http://85.215.9.83/es/OnePiece/Products/Singles/{collection}?idRarity=0&sortBy=collectorsnumber_asc&perSite=20"
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        for row in response.xpath('//*[contains(@class, "table-body")]/div'):
            urls = row.xpath('.//a/@href')
            yield scrapy.Request(url="http://85.215.9.83" + urls[1].get() + "?language=1&amount=4", callback=self.parse_detail)
        
        next = response.css('a[aria-label="Siguiente página"]::attr(href)').extract_first()
        if next is not None:
            next_page = response.urljoin(next)
            yield scrapy.Request(next_page, callback=self.parse)
        
    def parse_detail(self, response):
        title = response.xpath('//h1/text()').get()
        elements = response.xpath('//*[@class="col-6 col-xl-7"]')
        rarity = elements[0].xpath('.//@data-original-title').get()
        if rarity == 'DON!!':
            number = 'NULL'
            price = elements[7].xpath('.//text()').get()
        else:
            numbers = response.xpath('//*[@class="d-none d-md-block col-6 col-xl-7"]')
            number = numbers[0].xpath('.//text()').get()
            try:
                price = elements[8].xpath('.//text()').get()
            except:
                price = "N/A"
        # img = response.xpath('//div[@class="image card-image is-onepiece w-100"]/img/@src')

        individual_prices =  response.xpath('//*[@class="color-primary small text-end text-nowrap fw-bold "]/text()')
        try:
            playset_price = individual_prices[0].extract()
        except:
            playset_price = "N/A"

        yield {
            'name': title,
            'collection': elements[1].xpath('.//text()').get(),
            'number': number,
            'rarity': rarity,
            # 'link': response.url,
            # 'img': img.get(),
            'price': price,
            'playset_price': playset_price
        }
