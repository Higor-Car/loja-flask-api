import bcrypt
import os
import psycopg2

def connect():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    name = os.getenv("DB_NAME")
    password = os.getenv("DB_PASSWORD")
    bancoDados = psycopg2.connect(host=host, port=port, user=user, dbname=name, password=password)
    return bancoDados

def inserirProduto(nome,preco,descricao,quantidade):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""INSERT INTO produtos(nome,preco,descricao,quantidade) VALUES(%s,%s,%s,%s) RETURNING id""", (nome,preco,descricao,quantidade))
        bancoDados.commit()
        novoId = cursor.fetchone()[0]
    finally:
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
    return dict(zip(colunas, produtoEspecifico)) if produtoEspecifico else None

def atualizarProduto(nome,preco,descricao,quantidade,id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""UPDATE produtos SET nome = %s, preco= %s,descricao= %s, quantidade = %s WHERE id = %s""",(nome, preco, descricao, quantidade,id))
        bancoDados.commit()
    finally:
        bancoDados.close()

def deletarProduto(id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""DELETE FROM produtos WHERE id = %s""", (id,))
        bancoDados.commit()
    finally:
        bancoDados.close()



def inserirCliente(nome, email, senha):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        senhaHash = (bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())).decode("utf-8")
        cursor.execute("""INSERT INTO cliente(nome, email, senha)VALUES (%s, %s, %s) RETURNING id""", (nome, email, senhaHash))
        bancoDados.commit()
        novoId = cursor.fetchone()[0]
    finally:
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
    return dict(zip(colunas, clienteEspecifico)) if clienteEspecifico else None

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
    try:
        senhaHash = (bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())).decode("utf-8")
        cursor.execute("""UPDATE cliente SET nome= %s,email= %s,senha= %s WHERE id = %s""", (nome, email, senhaHash, id))
        bancoDados.commit()
    finally:
        bancoDados.close()

def deletarCliente(id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""DELETE FROM cliente WHERE id = %s""", (id,))
        bancoDados.commit()
    finally:
        bancoDados.close()



def inserirPedido(cliente_id, data):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""INSERT INTO pedido(cliente_id,data)VALUES(%s,%s) RETURNING id""",(cliente_id,data))
        bancoDados.commit()
        novoId = cursor.fetchone()[0]
    finally:
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
    return dict(zip(colunas, pedidoEspecifico)) if pedidoEspecifico else None

def atualizarPedido(cliente_id, data, id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""UPDATE pedido SET cliente_id = %s,data = %s WHERE id = %s""",(cliente_id,data,id))
        bancoDados.commit()
    finally:
        bancoDados.close()

def deletarPedido(id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""DELETE FROM pedido WHERE id=%s""",(id,))
        bancoDados.commit()
    finally:
        bancoDados.close()


def inserirItensPedido(pedido_id,produto_id,quantidade):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""INSERT INTO itensPedido(pedido_id,produto_id,quantidade)VALUES(%s,%s,%s) RETURNING id""",(pedido_id,produto_id,quantidade))
        bancoDados.commit()
        novoId = cursor.fetchone()[0]
    finally:
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
    return dict(zip(colunas, itensPedidoEspecifico)) if itensPedidoEspecifico else None

def atualizarItensPedido(pedido_id, produto_id,quantidade, id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""UPDATE itensPedido SET pedido_id = %s,produto_id = %s,quantidade = %s WHERE id = %s""",(pedido_id,produto_id,quantidade,id))
        bancoDados.commit()
    finally:
        bancoDados.close()

def deletarItensPedidos(id):
    bancoDados = connect()
    cursor = bancoDados.cursor()
    try:
        cursor.execute("""DELETE FROM itensPedido WHERE id = %s""",(id,))
        bancoDados.commit()
    finally:
        bancoDados.close()

def criarPedidoCompleto(cliente_id, data, itens):
    if not itens:
        raise ValueError("O pedido precisa ter ao menos um item")

    quantidades = {}
    for item in itens:
        if item["quantidade"] <= 0:
            raise ValueError("A quantidade de cada item deve ser maior que zero")
        produto_id = item["produto_id"]
        quantidades[produto_id] = quantidades.get(produto_id, 0) + item["quantidade"]

    bancoDados = connect()
    cursor = bancoDados.cursor()

    try:
        # Trava os produtos em ordem fixa para compras simultâneas não venderem o mesmo estoque.
        cursor.execute(
            """SELECT id, nome, quantidade FROM produtos WHERE id = ANY(%s) ORDER BY id FOR UPDATE""",
            (sorted(quantidades),)
        )
        produtos = {id: (nome, estoque) for id, nome, estoque in cursor.fetchall()}

        for produto_id, quantidade in quantidades.items():
            if produto_id not in produtos:
                raise ValueError(f"Produto {produto_id} não existe")
            nome, estoque = produtos[produto_id]
            if estoque < quantidade:
                raise ValueError(f"Estoque insuficiente para {nome}")

        cursor.execute("""INSERT INTO pedido(cliente_id,data)VALUES(%s,%s) RETURNING id""", (cliente_id, data))
        pedido_id = cursor.fetchone()[0]

        for produto_id, quantidade in quantidades.items():
            cursor.execute(
                """INSERT INTO itensPedido(pedido_id,produto_id,quantidade)VALUES(%s,%s,%s)""",
                (pedido_id, produto_id, quantidade)
            )
            cursor.execute(
                """UPDATE produtos SET quantidade = quantidade - %s WHERE id = %s""",
                (quantidade, produto_id)
            )
        bancoDados.commit()
        return pedido_id

    except Exception:
        bancoDados.rollback()
        raise
    finally:
        bancoDados.close()