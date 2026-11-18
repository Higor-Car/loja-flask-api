from app.models.loja_db import connect
from dotenv import load_dotenv

def criarTabelas():
    load_dotenv()
    bancoDados=connect()
    try:
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

    finally:
        bancoDados.close()

if __name__ == "__main__":
    criarTabelas()