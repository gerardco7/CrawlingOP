import subprocess
    
def run_spider():
    subprocess.run(["scrapy", "crawl", "cardmarket"])

if __name__ == "__main__":
    run_spider()

    
