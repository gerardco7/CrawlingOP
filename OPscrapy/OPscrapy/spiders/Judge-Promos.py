import scrapy
from urllib.parse import urlencode
from scrapy.shell import inspect_response
from time import sleep

# TODO: conseguir imagen i link
# TODO: pasar a base de datos
# TODO: hacerlo para todas las cartas

# scrapy crawl cardmarket -o cardmarket.json

class CardmarketSpider(scrapy.Spider):
    name = "Judge-Promos"
    allowed_domains = ["85.215.9.83"]

    def start_requests(self):
        url = "http://85.215.9.83/es/OnePiece/Products/Singles?idCategory=1621&idExpansion=0&idRarity=0&sortBy=collectorsnumber_asc&perSite=20"
        yield scrapy.Request(url=url, callback=self.collections)

    def collections(self, response):
        collection = "Judge-Promos"
        url = f"http://85.215.9.83/es/OnePiece/Products/Singles/{collection}?idRarity=0&sortBy=collectorsnumber_asc&perSite=20"
        yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        for row in response.xpath('//*[contains(@class, "table-body")]/div'):
            urls = row.xpath('.//a/@href')
            yield scrapy.Request(url="http://85.215.9.83" + urls[1].get(), callback=self.parse_detail)
        sleep(60)  # Add a delay of 1 minute
        
        next = response.css('a[aria-label="Siguiente página"]::attr(href)').extract_first()
        if next is not None:
            next_page = response.urljoin(next)
            yield scrapy.Request(next_page, callback=self.parse)
        
    def parse_detail(self, response):
        # if 429 response, retry after 60 seconds
        if response.status == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            self.logger.warning(f"Received 429 response. Retrying after {retry_after} seconds.")
            sleep(retry_after)
            yield scrapy.Request(response.url, callback=self.parse_detail)
        else:
            title = response.xpath('//h1/text()').get()
            elements = response.xpath('//*[@class="col-6 col-xl-7"]')
            rarity = elements[0].xpath('.//@data-original-title').get()
            if rarity == 'DON!!':
                number = 'NULL'
                price = elements[5].xpath('.//text()').get()
            else:
                number = elements[3].xpath('.//text()').get()
                price = elements[6].xpath('.//text()').get()
            # img = response.xpath('//div[@class="image card-image is-onepiece w-100"]/img/@src')
            yield {
                'name': title,
                'colection': elements[1].xpath('.//text()').get(),
                'number': number,
                'rarity': rarity,
                # 'link': response.url,
                # 'img': img.get(),
                'price': price,
        }
