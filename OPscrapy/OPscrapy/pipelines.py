# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import psycopg2


class OpscrapyPipeline:

    def open_spider(self, spider):
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="bruno202122"
        )
        self.cur = conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        
    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO cartasOP (name, collection, rarity, number, price)
            VALUES (%s, %s, %s, %s, %s)
        """, (item['name'], item['colection'], item['rarity'], item['number'], item['price']))
        return item
