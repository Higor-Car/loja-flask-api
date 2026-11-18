from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import current_user, jwt_required
from app.models.loja_db import buscarPedidosDoCliente, buscarPedidoDoCliente, inserirPedido, atualizarPedido, deletarPedido
from app.schemas.schemas import PedidoSchema

blp = Blueprint("pedidos", __name__, description="Operações de pedidos")


def buscarPedidoAutorizado(id):
    pedido = buscarPedidoDoCliente(id, current_user["id"])
    if not pedido:
        abort(404, message="Pedido não encontrado")
    return pedido


@blp.route("/pedidos")
class PedidoLista(MethodView):

    @jwt_required()
    @blp.response(200, PedidoSchema(many=True))
    def get(self):
        return buscarPedidosDoCliente(current_user["id"])

    @jwt_required()
    @blp.arguments(PedidoSchema)
    @blp.response(201, PedidoSchema)
    def post(self, dados):
        id = inserirPedido(current_user["id"], dados["data"])
        return {**dados, "id": id, "cliente_id": current_user["id"]}


@blp.route("/pedidos/<int:id>")
class Pedido(MethodView):

    @jwt_required()
    @blp.response(200, PedidoSchema)
    def get(self, id):
        return buscarPedidoAutorizado(id)

    @jwt_required()
    @blp.arguments(PedidoSchema)
    @blp.response(200, PedidoSchema)
    def put(self, dados, id):
        buscarPedidoAutorizado(id)
        atualizarPedido(current_user["id"], dados["data"], id)
        return {**dados, "id": id, "cliente_id": current_user["id"]}

    @jwt_required()
    @blp.response(200)
    def delete(self, id):
        buscarPedidoAutorizado(id)
        deletarPedido(id)
        return {"mensagem": f"Pedido com id {id} deletado com sucesso"}
