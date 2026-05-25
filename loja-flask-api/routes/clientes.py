from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from loja_db import buscarTodosOsClientes,buscarUmCliente,inserirCliente,atualizarCliente,deletarCliente
from schemas import ClienteSchema

blp = Blueprint("cliente", __name__, description="Operações de cliente")

@blp.route("/cliente")
class ClienteLista(MethodView):

    @blp.response(200, ClienteSchema(many=True))
    def get(self):
        return buscarTodosOsClientes()

    @jwt_required()
    @blp.arguments(ClienteSchema)
    @blp.response(201, ClienteSchema)
    def post(self, dados):
        id = inserirCliente(dados["nome"], dados["email"], dados["senha"])
        return {**dados, "id": id}


@blp.route("/cliente/<int:id>")
class Cliente (MethodView):

    @blp.response(200, ClienteSchema)
    def get(self, id):
        cliente = buscarUmCliente(id)
        if not cliente:
            abort(404, message="Cliente não encontrado")
        return cliente

    @jwt_required()
    @blp.arguments(ClienteSchema)
    @blp.response(200, ClienteSchema)
    def put(self, dados, id):
        atualizarCliente(dados["nome"], dados["email"], dados["senha"], id)
        return {**dados, "id": id}

    @jwt_required()
    @blp.response(200)
    def delete(self, id):
        deletarCliente(id)
        return {"mensagem": f"Cliente com id {id} deletado com sucesso"}