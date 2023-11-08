import scrapy
from urllib.parse import urlencode
from scrapy.shell import inspect_response

# TODO: conseguir imagen i link
# TODO: pasar a base de datos

API_KEY = "8586126d-c4df-45d9-a49d-2d0c3e10d72f"

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class CardmarketSpider(scrapy.Spider):
    name = "cardmarket"
    allowed_domains = ["cardmarket.com", "proxy.scrapeops.io"]
    start_url = ["https://www.cardmarket.com/en/OnePiece/Products/Singles"]

    def start_requests(self):
        urls = ["https://www.cardmarket.com/en/OnePiece/Products/Singles?idCategory=1621&idExpansion=0&idRarity=0&sortBy=collectorsnumber_asc"]
        for url in urls:
            yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse)
    
    def parse(self, response):
        for row in response.xpath('//*[contains(@class, "table-body")]/div'):
            urls = row.xpath('.//a/@href')
            yield scrapy.Request(url=get_scrapeops_url("https://www.cardmarket.com/" + urls[1].get()), callback=self.parse_detail)

    def parse_detail(self, response):
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
        
