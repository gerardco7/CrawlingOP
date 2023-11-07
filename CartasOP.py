import psycopg2

def createtable():
    # Crear un cursor para ejecutar comandos en la base de datos
    cur = conn.cursor()

    # Crear la tabla cartasOP
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cardsop (
            card_id SERIAL PRIMARY KEY,
            name VARCHAR(30),
            collection VARCHAR(255),
            number INT,
            rarity VARCHAR(20),
            link VARCHAR(255),
            img VARCHAR(255),
            price INT
        );
    """)

    # Cerrar el cursor  a la base de datos
    cur.close()

# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="CardsOP",
    user="postgres",
    password="bruno202122"
)



