from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import current_user, jwt_required
from app.models.loja_db import buscarItensDoCliente,buscarItemDoCliente,buscarPedidoDoCliente,inserirItensPedido,atualizarItensPedido,deletarItensPedidos
from app.schemas.schemas import ItensPedidoSchema

blp = Blueprint("itensPedidos", __name__, description="Operações de itens produtos")


def buscarItemAutorizado(id):
    item = buscarItemDoCliente(id, current_user["id"])
    if not item:
        abort(404, message="Pedido de itens não encontrado")
    return item


def exigirPedidoDoCliente(pedido_id):
    if not buscarPedidoDoCliente(pedido_id, current_user["id"]):
        abort(404, message="Pedido não encontrado")


@blp.route("/itensPedidos")
class ItensPedidoLista(MethodView):

    @jwt_required()
    @blp.response(200, ItensPedidoSchema(many=True))
    def get(self):
        return buscarItensDoCliente(current_user["id"])

    @jwt_required()
    @blp.arguments(ItensPedidoSchema)
    @blp.response(201, ItensPedidoSchema)
    def post(self, dados):
        exigirPedidoDoCliente(dados["pedido_id"])
        id = inserirItensPedido(dados["pedido_id"], dados["produto_id"], dados["quantidade"])
        return {**dados, "id": id}


@blp.route("/itensPedidos/<int:id>")
class ItensPedido(MethodView):

    @jwt_required()
    @blp.response(200, ItensPedidoSchema)
    def get(self, id):
        return buscarItemAutorizado(id)

    @jwt_required()
    @blp.arguments(ItensPedidoSchema)
    @blp.response(200, ItensPedidoSchema)
    def put(self, dados, id):
        buscarItemAutorizado(id)
        exigirPedidoDoCliente(dados["pedido_id"])
        atualizarItensPedido(dados["pedido_id"], dados["produto_id"], dados["quantidade"], id)
        return {**dados, "id": id}

    @jwt_required()
    @blp.response(200)
    def delete(self, id):
        buscarItemAutorizado(id)
        deletarItensPedidos(id)
        return {"mensagem": f"Pedido de itens com id {id} deletado com sucesso"}
