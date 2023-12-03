import subprocess

def run_spider(spider_name):
    subprocess.run(["scrapy", "crawl", spider_name])
    print(f"{spider_name} completed!")

if __name__ == "__main__":
    spider_names = ["Awakening-of-the-New-Era", "Judge-Promos", "Kingdoms-of-Intrigue", "One-Piece-Products", "Paramount-War", "Pillars-of-Strength", "Premium-Bandai-Products"]

    for spider_name in spider_names:
        run_spider(spider_name)