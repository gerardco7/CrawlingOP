from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def crawler_process():
    process = CrawlerProcess(get_project_settings())
    process.crawl('cardmarket')
    process.start()

if __name__ == "__main__":
    crawler_process()
