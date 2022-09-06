import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()

cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY, " \
              "nome TEXT, estrelas REAL, diaria REAL, cidade TEXT)"
cria_hotel = "INSERT INTO hoteis VALUES('alpha', 'Alpha Hotel', '4.3', '450.35', 'Rio de Janeiro')"

cursor.execute(cria_tabela)
#cursor.execute(cria_hotel)

connection.commit()
connection.close()

