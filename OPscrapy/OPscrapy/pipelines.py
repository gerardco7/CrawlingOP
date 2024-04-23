import psycopg2
import datetime
from itemadapter import ItemAdapter


class OpscrapyPipeline:

    def open_spider(self, spider):
        self.first_item = True

        with open("DBpassword.txt", "r") as file:
                contraseña = file.read().strip()

        self.conn = psycopg2.connect(
            host="localhost",
            database="CardsOP",
            user="postgres",
            password=contraseña
           
        )
        self.cur = self.conn.cursor()

        # Check if table cardsop exists
        self.cur.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = 'cardsop'
            )
        """)
        cardsop_exists = self.cur.fetchone()[0]

        # If table doesn't exist, create it. 
        if not cardsop_exists:
            # Create card table
            self.cur.execute("""
                CREATE TABLE cardsop (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    collection VARCHAR(255),
                    number INT,
                    rarity VARCHAR(255),
                    link VARCHAR(255),
                    img VARCHAR(255)
                )
            """)
            self.conn.commit()

        self.cur.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = 'priceop'
            )
        """)
        priceop_exists = self.cur.fetchone()[0]

        if not priceop_exists:
            # Create price table
            self.cur.execute("""
                CREATE TABLE priceop (
                    id SERIAL PRIMARY KEY,
                    card_id INT,
                    price FLOAT,
                    playset_price FLOAT,
                    day VARCHAR(255),
                    month VARCHAR(255),
                    year VARCHAR(255),
                    time VARCHAR(255),
                    FOREIGN KEY (card_id) REFERENCES cardsop (id)
                )
            """)
            self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['number'] == 'NULL':
            adapter['number'] = '0'
        elif not adapter['number'].isdigit():
            adapter['number'] = int(adapter['number'][-3:])
        else:
            adapter['number'] = int(adapter['number'])

        if adapter['price'] != "N/A":
            adapter['price'] = adapter['price'].replace('.', '')
            adapter['price'] = adapter['price'].replace(' €', '')  
            adapter['price'] = adapter['price'].replace(',', '.')  
            adapter['price'] = float(adapter['price'])
        else:
            adapter['price'] = 0.0

        if adapter['playset_price'] != "N/A":
            adapter['playset_price'] = adapter['playset_price'].replace('.', '')
            adapter['playset_price'] = adapter['playset_price'].replace(' €', '')  
            adapter['playset_price'] = adapter['playset_price'].replace(',', '.')  
            adapter['playset_price'] = float(adapter['playset_price'])
        else:
            adapter['playset_price'] = 0.0

        # Get the current date. Format day, month, and year as DD/MM/YYYY
        current_date = datetime.datetime.now()
        adapter['day'] = current_date.day
        adapter['month'] = current_date.month
        adapter['year'] = current_date.year
        adapter['time'] = current_date.strftime("%H:%M:%S")

        # Check if card exists in the database
        self.cur.execute("""
            SELECT id
            FROM cardsop
            WHERE name = %s AND collection = %s AND number = %s
        """, (item['name'], item['collection'], adapter['number']))

        result = self.cur.fetchone()
        card_id = result[0] if result else None 

        if card_id is None:
            self.cur.execute("""
                INSERT INTO cardsop (name, collection, number, rarity)
                VALUES (%s, %s, %s, %s)
            """, (item['name'], item['collection'], adapter['number'], item['rarity']))
            self.conn.commit()
            self.cur.execute("""
                SELECT id
                FROM cardsop
                WHERE name = %s AND collection = %s AND number = %s
            """, (item['name'], item['collection'], adapter['number']))
            result = self.cur.fetchone()
            card_id = result[0]

        self.cur.execute("""
            INSERT INTO priceop (card_id, price, playset_price, day, month, year, time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (card_id, adapter['price'], adapter['playset_price'], adapter['day'], adapter['month'], adapter['year'], adapter['time']))
        self.conn.commit()

        return item
