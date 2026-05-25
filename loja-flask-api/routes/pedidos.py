from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from loja_db import buscarTodosOsPedidos, buscarUmPedido, inserirPedido, atualizarPedido, deletarPedido
from schemas import PedidoSchema

blp = Blueprint("pedidos", __name__, description="Operações de pedidos")

@blp.route("/pedidos")
class PedidoLista(MethodView):

    @blp.response(200, PedidoSchema(many=True))
    def get(self):
        return buscarTodosOsPedidos()

    @jwt_required()
    @blp.arguments(PedidoSchema)
    @blp.response(201, PedidoSchema)
    def post(self, dados):
        id = inserirPedido(dados["cliente_id"], dados["data"])
        return {**dados, "id": id}


@blp.route("/pedidos/<int:id>")
class Pedido(MethodView):

    @blp.response(200, PedidoSchema)
    def get(self, id):
        pedido = buscarUmPedido(id)
        if not pedido:
            abort(404, message="Pedido não encontrado")
        return pedido

    @jwt_required()
    @blp.arguments(PedidoSchema)
    @blp.response(200, PedidoSchema)
    def put(self, dados, id):
        atualizarPedido(dados["cliente_id"], dados["data"], id)
        return {**dados, "id": id}

    @jwt_required()
    @blp.response(200)
    def delete(self, id):
        deletarPedido(id)
        return {"mensagem": f"Pedido com id {id} deletado com sucesso"}