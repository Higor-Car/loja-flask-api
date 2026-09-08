import sqlite3
import bcrypt

def inserirProduto(nome,preco,descricao,quantidade):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""INSERT INTO produtos(nome,preco,descricao,quantidade) VALUES(?,?,?,?)""", (nome,preco,descricao,quantidade))
    bancoDados.commit()
    novoId = cursor.lastrowid
    bancoDados.close()
    return novoId

def buscarTodosOsProdutos():
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""SELECT * FROM produtos""")
    todosOsProdutos = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, linha)) for linha in todosOsProdutos]

def buscarUmProduto(id):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""SELECT * FROM produtos WHERE id = ?""", (id,))
    produtoEspecifico = cursor.fetchone()
    colunas = [desc[0] for desc in cursor.description]
    return dict(zip(colunas, produtoEspecifico))

def atualizarProduto(nome,preco,descricao,quantidade,id):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""UPDATE produtos SET nome = ?, preco= ?,descricao= ?, quantidade = ? WHERE id = ?""",(nome, preco, descricao, quantidade,id))
    bancoDados.commit()
    bancoDados.close()

def deletarProduto(id):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""DELETE FROM produtos WHERE id = ?""", (id,))
    bancoDados.commit()
    bancoDados.close()



def inserirCliente(nome, email, senha):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    senhaHash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
    cursor.execute("""INSERT INTO cliente(nome, email, senha)VALUES (?, ?, ?)""", (nome, email, senhaHash))
    bancoDados.commit()
    novoId = cursor.lastrowid
    bancoDados.close()
    return novoId

def buscarTodosOsClientes():
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""SELECT * FROM cliente""")
    todosOsClientes = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, linha)) for linha in todosOsClientes]

def buscarUmCliente(id):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""SELECT * FROM cliente WHERE id = ?""", (id,))
    clienteEspecifico = cursor.fetchone()
    colunas = [desc[0] for desc in cursor.description]
    return dict(zip(colunas, clienteEspecifico))

def buscarClientePorEmail(email,senha):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""SELECT * FROM cliente WHERE email = ?""", (email,))
    clienteEmail = cursor.fetchone()
    if clienteEmail == None:
        return None
    colunas = [desc[0] for desc in cursor.description]
    clienteDict = dict(zip(colunas, clienteEmail))
    senhaCorreta = bcrypt.checkpw(senha.encode("utf-8"), clienteDict["senha"])
    if not senhaCorreta:
        return None
    return clienteDict

def atualizarCliente(nome,email,senha,id):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    senhaHash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
    cursor.execute("""UPDATE cliente SET nome= ?,email= ?,senha= ? WHERE id = ?""", (nome, email, senhaHash, id))
    bancoDados.commit()
    bancoDados.close()

def deletarCliente(id):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""DELETE FROM cliente WHERE id = ?""", (id,))
    bancoDados.commit()
    bancoDados.close()



def inserirPedido(cliente_id, data):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""INSERT INTO pedido(cliente_id,data)VALUES(?,?)""",(cliente_id,data))
    bancoDados.commit()
    novoId = cursor.lastrowid
    bancoDados.close()
    return novoId

def buscarTodosOsPedidos():
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""SELECT * FROM pedido""")
    todosOsPedidos = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, linha)) for linha in todosOsPedidos]

def buscarUmPedido(id):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""SELECT * FROM pedido WHERE id=?""",(id,))
    pedidoEspecifico = cursor.fetchone()
    colunas = [desc[0] for desc in cursor.description]
    return dict(zip(colunas, pedidoEspecifico))

def atualizarPedido(cliente_id, data, id):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""UPDATE pedido SET cliente_id = ?,data = ? WHERE id = ?""",(cliente_id,data,id))
    bancoDados.commit()
    bancoDados.close()

def deletarPedido(id):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""DELETE FROM pedido WHERE id=?""",(id,))
    bancoDados.commit()
    bancoDados.close()


def inserirItensPedido(pedido_id,produto_id,quantidade):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""INSERT INTO itensPedido(pedido_id,produto_id,quantidade)VALUES(?,?,?)""",(pedido_id,produto_id,quantidade))
    bancoDados.commit()
    novoId = cursor.lastrowid
    bancoDados.close()
    return novoId

def buscarTodosOsItensPedidos():
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""SELECT * FROM itensPedido""")
    todosOsItensPedidos = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    return [dict(zip(colunas, linha)) for linha in todosOsItensPedidos]

def buscarItensPedido(id):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""SELECT * FROM itensPedido WHERE id=?""",(id,))
    itensPedidoEspecifico = cursor.fetchone()
    colunas = [desc[0] for desc in cursor.description]
    return dict(zip(colunas, itensPedidoEspecifico))

def atualizarItensPedido(pedido_id, produto_id,quantidade, id):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""UPDATE itensPedido SET pedido_id = ?,produto_id = ?,quantidade = ? WHERE id = ?""",(pedido_id,produto_id,quantidade,id))
    bancoDados.commit()
    bancoDados.close()

def deletarItensPedidos(id):
    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()
    cursor.execute("""DELETE FROM itensPedido WHERE id = ?""",(id,))
    bancoDados.commit()
    bancoDados.close()

def criarPedidoCompleto(cliente_id, data, itens):

    bancoDados = sqlite3.connect("../../banco-dados-loja.db")
    cursor = bancoDados.cursor()

    try:

        cursor.execute("""SELECT * FROM produtos""")
        todos = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
        produtos = {p["id"]: p for p in [dict(zip(colunas, linha)) for linha in todos]}

        for item in itens:
            produto = produtos.get(item["produto_id"])
            if produto is None:
                raise ValueError(f"Produto {item['produto_id']} não existe")
            if produto["quantidade"] < item["quantidade"]:
                raise ValueError(f"Estoque insuficiente para {produto['nome']}")

        cursor.execute("""INSERT INTO pedido(cliente_id,data)VALUES(?,?)""", (cliente_id, data))
        pedido_id = cursor.lastrowid

        for item in itens:
            cursor.execute(
                """INSERT INTO itensPedido(pedido_id,produto_id,quantidade)VALUES(?,?,?)""",
                (pedido_id, item["produto_id"], item["quantidade"])
            )
            nova_quantidade = produtos[item["produto_id"]]["quantidade"] - item["quantidade"]
            cursor.execute(
                """UPDATE produtos SET quantidade = ? WHERE id = ?""",
                (nova_quantidade, item["produto_id"])
            )

        bancoDados.commit()
        return pedido_id

    except Exception:
        bancoDados.rollback()
        raise
    finally:
        bancoDados.close()


