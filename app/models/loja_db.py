import bcrypt
from schema import connect

def inserirProduto(nome,preco,descricao,quantidade):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    cursor.execute("""INSERT INTO produtos(nome,preco,descricao,quantidade) VALUES(%s,%s,%s,%s) RETURNING id""", (nome,preco,descricao,quantidade))
    bancoDados.commit()
    novoId = cursor.fetchone()[0]
    bancoDados.close()
    return novoId

def buscarTodosOsProdutos():
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""SELECT * FROM produtos""")
        todosOsProdutos = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        bancoDados.close()
    return [dict(zip(colunas, linha)) for linha in todosOsProdutos]

def buscarUmProduto(id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""SELECT * FROM produtos WHERE id = %s""", (id,))
        produtoEspecifico = cursor.fetchone()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        bancoDados.close()
    return dict(zip(colunas, produtoEspecifico))

def atualizarProduto(nome,preco,descricao,quantidade,id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    cursor.execute("""UPDATE produtos SET nome = %s, preco= %s,descricao= %s, quantidade = %s WHERE id = %s""",(nome, preco, descricao, quantidade,id))
    bancoDados.commit()
    bancoDados.close()

def deletarProduto(id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    cursor.execute("""DELETE FROM produtos WHERE id = %s""", (id,))
    bancoDados.commit()
    bancoDados.close()



def inserirCliente(nome, email, senha):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    senhaHash = (bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())).decode("utf-8")
    cursor.execute("""INSERT INTO cliente(nome, email, senha)VALUES (%s, %s, %s) RETURNING id""", (nome, email, senhaHash))
    bancoDados.commit()
    novoId = cursor.fetchone()[0]
    bancoDados.close()
    return novoId

def buscarTodosOsClientes():
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""SELECT * FROM cliente""")
        todosOsClientes = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        bancoDados.close()
    return [dict(zip(colunas, linha)) for linha in todosOsClientes]

def buscarUmCliente(id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""SELECT * FROM cliente WHERE id = %s""", (id,))
        clienteEspecifico = cursor.fetchone()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        bancoDados.close()
    return dict(zip(colunas, clienteEspecifico))

def buscarClientePorEmail(email,senha):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""SELECT * FROM cliente WHERE email = %s""", (email,))
        clienteEmail = cursor.fetchone()
        if clienteEmail is None:
            return None
        colunas = [desc[0] for desc in cursor.description]
        clienteDict = dict(zip(colunas, clienteEmail))
        senhaCorreta = bcrypt.checkpw(senha.encode("utf-8"), clienteDict["senha"].encode("utf-8"))
        if not senhaCorreta:
            return None
    finally:
        bancoDados.close()
    return clienteDict

def atualizarCliente(nome,email,senha,id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    senhaHash = (bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())).decode("utf-8")
    cursor.execute("""UPDATE cliente SET nome= %s,email= %s,senha= %s WHERE id = %s""", (nome, email, senhaHash, id))
    bancoDados.commit()
    bancoDados.close()

def deletarCliente(id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    cursor.execute("""DELETE FROM cliente WHERE id = %s""", (id,))
    bancoDados.commit()
    bancoDados.close()



def inserirPedido(cliente_id, data):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    cursor.execute("""INSERT INTO pedido(cliente_id,data)VALUES(%s,%s) RETURNING id""",(cliente_id,data))
    bancoDados.commit()
    novoId = cursor.fetchone()[0]
    bancoDados.close()
    return novoId

def buscarTodosOsPedidos():
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""SELECT * FROM pedido""")
        todosOsPedidos = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        bancoDados.close()
    return [dict(zip(colunas, linha)) for linha in todosOsPedidos]

def buscarUmPedido(id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""SELECT * FROM pedido WHERE id=%s""",(id,))
        pedidoEspecifico = cursor.fetchone()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        bancoDados.close()
    return dict(zip(colunas, pedidoEspecifico))

def atualizarPedido(cliente_id, data, id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    cursor.execute("""UPDATE pedido SET cliente_id = %s,data = %s WHERE id = %s""",(cliente_id,data,id))
    bancoDados.commit()
    bancoDados.close()

def deletarPedido(id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    cursor.execute("""DELETE FROM pedido WHERE id=%s""",(id,))
    bancoDados.commit()
    bancoDados.close()


def inserirItensPedido(pedido_id,produto_id,quantidade):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    cursor.execute("""INSERT INTO itensPedido(pedido_id,produto_id,quantidade)VALUES(%s,%s,%s) RETURNING id""",(pedido_id,produto_id,quantidade))
    bancoDados.commit()
    novoId = cursor.fetchone()[0]
    bancoDados.close()
    return novoId

def buscarTodosOsItensPedidos():
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""SELECT * FROM itensPedido""")
        todosOsItensPedidos = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        bancoDados.close()
    return [dict(zip(colunas, linha)) for linha in todosOsItensPedidos]

def buscarItensPedido(id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""SELECT * FROM itensPedido WHERE id=%s""",(id,))
        itensPedidoEspecifico = cursor.fetchone()
        colunas = [desc[0] for desc in cursor.description]
    finally:
        bancoDados.close()
    return dict(zip(colunas, itensPedidoEspecifico))

def atualizarItensPedido(pedido_id, produto_id,quantidade, id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    cursor.execute("""UPDATE itensPedido SET pedido_id = %s,produto_id = %s,quantidade = %s WHERE id = %s""",(pedido_id,produto_id,quantidade,id))
    bancoDados.commit()
    bancoDados.close()

def deletarItensPedidos(id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    cursor.execute("""DELETE FROM itensPedido WHERE id = %s""",(id,))
    bancoDados.commit()
    bancoDados.close()

def criarPedidoCompleto(cliente_id, data, itens):

    bancoDados = connect()
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

        cursor.execute("""INSERT INTO pedido(cliente_id,data)VALUES(%s,%s) RETURNING id""", (cliente_id, data))
        pedido_id = cursor.fetchone()[0]

        for item in itens:
            cursor.execute(
                """INSERT INTO itensPedido(pedido_id,produto_id,quantidade)VALUES(%s,%s,%s)""",
                (pedido_id, item["produto_id"], item["quantidade"])
            )
            nova_quantidade = produtos[item["produto_id"]]["quantidade"] - item["quantidade"]
            cursor.execute(
                """UPDATE produtos SET quantidade = %s WHERE id = %s""",
                (nova_quantidade, item["produto_id"])
            )
        bancoDados.commit()
        return pedido_id

    except Exception:
        bancoDados.rollback()
        raise
    finally:
        bancoDados.close()