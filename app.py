from flask import request,Flask,jsonify,json
from flask_jwt_extended import JWTManager, create_access_token,jwt_required
from loja_db import buscarTodosOsProdutos,buscarUmProduto,inserirProduto,atualizarProduto,deletarProduto
from loja_db import buscarTodosOsClientes,buscarUmCliente,inserirCliente,atualizarCliente,deletarCliente
from loja_db import buscarTodosOsItensPedidos,buscarItensPedido,inserirItensPedido,atualizarItensPedido,deletarItensPedidos
from loja_db import buscarTodosOsPedidos,buscarUmPedido,inserirPedido,atualizarPedido,deletarPedido
from loja_db import buscarClientePorEmail

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "kj#92@xLp!mQ3z"
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    dados = request.json
    email = dados.get("email")
    senha = dados.get("senha")
    buscarClienteEmail = buscarClientePorEmail(email,senha)
    if buscarClienteEmail == None:
        return jsonify({"mensagem":"Cliente não encontrado"}),401
    else:
        return jsonify(create_access_token(email))

@app.route("/produtos", methods=["GET"])
def listarProdutos():
    produtos=buscarTodosOsProdutos()
    return jsonify(produtos), 200

@app.route("/produtos/<int:id>", methods=["GET"])
def listarProduto(id):
    produto=buscarUmProduto (id)
    return jsonify(produto), 200

@app.route("/produtos", methods=["POST"])
@jwt_required()
def adicionarProduto():
    dados = request.json
    nome = dados.get("nome")
    preco = dados.get("preco")
    descricao = dados.get("descricao")
    quantidade = dados.get("quantidade")
    addProduto = inserirProduto(nome,preco,descricao,quantidade)
    return jsonify({"mensagem":"Produto criado","id": addProduto}), 201

@app.route("/produtos/<int:id>", methods=["PUT"])
@jwt_required()
def editarProduto(id):
    dados = request.json
    nome = dados.get("nome")
    preco = dados.get("preco")
    descricao = dados.get("descricao")
    quantidade = dados.get("quantidade")
    attProduto = atualizarProduto(nome,preco,descricao,quantidade,id)
    return jsonify({"mensagem": f"Produto com id {id} atualizado com sucesso"}), 200

@app.route("/produtos/<int:id>", methods=["DELETE"])
@jwt_required()
def excluirProduto(id):
    delProduto = deletarProduto(id)
    return jsonify({"mensagem" : f"Produto com id {id} foi deletado com sucesso"}),200

#Separar produto de cliente

@app.route("/clientes", methods=["GET"])
def listarClientes():
    clientes=buscarTodosOsClientes()
    return jsonify(clientes), 200

@app.route("/clientes/<int:id>", methods=["GET"])
def listarCliente(id):
    cliente=buscarUmCliente(id)
    return jsonify(cliente), 200

@app.route("/clientes", methods=["POST"])
@jwt_required()
def adicionarCliente():
    dados = request.json
    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")
    addCliente = inserirCliente(nome,email,senha)
    return jsonify({"mensagem":"Cliente criado","id": addCliente}), 201

@app.route("/clientes/<int:id>", methods=["PUT"])
@jwt_required()
def editarCliente(id):
    dados = request.json
    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")
    attProduto = atualizarCliente(nome,email,senha,id)
    return jsonify({"mensagem": f"Cliente com id {id} atualizado com sucesso"}), 200

@app.route("/clientes/<int:id>", methods=["DELETE"])
@jwt_required()
def excluirCliente(id):
    delCliente = deletarCliente(id)
    return jsonify({"mensagem" : f"Cliente com id {id} foi deletado com sucesso"}),200

#Separar cliente de pedidos

@app.route("/pedidos", methods=["GET"])
def listarPedidos():
    pedidos=buscarTodosOsPedidos()
    return jsonify(pedidos), 200

@app.route("/pedidos/<int:id>", methods=["GET"])
def listarPedido(id):
    pedido = buscarUmPedido(id)
    return jsonify(pedido), 200

@app.route("/pedidos", methods=["POST"])
@jwt_required()
def adicionarPedido():
    dados = request.json
    cliente_id = dados.get("cliente_id")
    data = dados.get("data")
    addPedido = inserirPedido(cliente_id,data)
    return jsonify({"mensagem":"Pedido criado","id": addPedido}), 201

@app.route("/pedidos/<int:id>", methods=["PUT"])
@jwt_required()
def editarPedido(id):
    dados = request.json
    cliente_id = dados.get("cliente_id")
    data = dados.get("data")
    attPedido = atualizarPedido(cliente_id, data,id)
    return jsonify({"mensagem": f"Pedido com id {id} atualizado com sucesso"}), 200

@app.route("/pedidos/<int:id>", methods=["DELETE"])
@jwt_required()
def excluirPedido(id):
    delCliente = deletarPedido(id)
    return jsonify({"mensagem" : f"Pedido com id {id} foi deletado com sucesso"}),200

#Separar pedidos de Itens Pedidos

@app.route("/itensPedidos", methods=["GET"])
def listarItensPedidos():
    itensPedidos=buscarTodosOsItensPedidos()
    return jsonify(itensPedidos), 200

@app.route("/itensPedidos/<int:id>", methods=["GET"])
def listarItenPedido(id):
    itenPedido=buscarItensPedido(id)
    return jsonify(itenPedido), 200

@app.route("/itensPedidos", methods=["POST"])
@jwt_required()
def adicionarItenPedido():
    dados = request.json
    pedido_id = dados.get("pedido_id")
    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade")
    addItensPedido = inserirItensPedido(pedido_id,produto_id,quantidade)
    return jsonify({"mensagem":"Itens Pedido criado","id": addItensPedido}), 201

@app.route("/itensPedidos/<int:id>", methods=["PUT"])
@jwt_required()
def editarItenPedido(id):
    dados = request.json
    pedido_id = dados.get("pedido_id")
    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade")
    attItensPedido = atualizarItensPedido(pedido_id,produto_id,quantidade,id)
    return jsonify({"mensagem": f"Itens Pedido com id {id} atualizado com sucesso"}), 200

@app.route("/itensPedidos/<int:id>", methods=["DELETE"])
@jwt_required()
def excluirItensPedido(id):
    delCliente = deletarItensPedidos(id)
    return jsonify({"mensagem" : f"Itens Pedidos com id {id} foi deletado com sucesso"}),200

if __name__ == "__main__":
    app.run(debug=True)


