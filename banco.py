import sqlite3

bancoDados = sqlite3.connect("banco-dados-loja.db")

cursor = bancoDados.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS produtos(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nome TEXT,
                      preco REAL,
                      descricao TEXT,
                      quantidade INTEGER)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS cliente(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nome TEXT,
                      email TEXT,
                      senha TEXT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS pedido(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      cliente_id INTEGER,
                      data TEXT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS itensPedido(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      pedido_id INTEGER,
                      produto_id INTEGER,
                      quantidade INTEGER)""")

bancoDados.commit()
