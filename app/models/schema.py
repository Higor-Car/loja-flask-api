import psycopg2
import os

def connect():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    name = os.getenv("DB_NAME")
    password = os.getenv("DB_PASSWORD")
    bancoDados = psycopg2.connect(host=host, port=port, user=user, dbname=name, password=password)
    return bancoDados

bancoDados = connect()

cursor = bancoDados.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS produtos(
                      id SERIAL PRIMARY KEY,
                      nome TEXT,
                      preco REAL,
                      descricao TEXT,
                      quantidade INTEGER)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS cliente(
                      id SERIAL PRIMARY KEY,
                      nome TEXT,
                      email TEXT,
                      senha TEXT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS pedido(
                      id SERIAL PRIMARY KEY,
                      cliente_id INTEGER,
                      data TEXT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS itensPedido(
                      id SERIAL PRIMARY KEY,
                      pedido_id INTEGER,
                      produto_id INTEGER,
                      quantidade INTEGER)""")

bancoDados.commit()