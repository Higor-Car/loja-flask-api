from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from loja_db import buscarTodosOsItensPedidos,buscarItensPedido,inserirItensPedido,atualizarItensPedido,deletarItensPedidos
from schemas import ItensPedidoSchema

blp = Blueprint("itensPedidos", __name__, description="Operações de itens produtos")

@blp.route("/itensPedidos")
class ItensPedidoLista(MethodView):

    @blp.response(200, ItensPedidoSchema(many=True))
    def get(self):
        return buscarTodosOsItensPedidos()

    @jwt_required()
    @blp.arguments(ItensPedidoSchema)
    @blp.response(201, ItensPedidoSchema)
    def post(self, dados):
        id = inserirItensPedido(dados["pedido_id"], dados["produto_id"], dados["quantidade"])
        return {**dados, "id": id}


@blp.route("/itensPedidos/<int:id>")
class ItensPedido(MethodView):

    @blp.response(200, ItensPedidoSchema)
    def get(self, id):
        itensPedido = buscarItensPedido(id)
        if not itensPedido:
            abort(404, message="Pedido de itens não encontrado")
        return itensPedido

    @jwt_required()
    @blp.arguments(ItensPedidoSchema)
    @blp.response(200, ItensPedidoSchema)
    def put(self, dados, id):
        atualizarItensPedido(dados["pedido_id"], dados["produto_id"], dados["quantidade"], id)
        return {**dados, "id": id}

    @jwt_required()
    @blp.response(200)
    def delete(self, id):
        deletarItensPedidos(id)
        return {"mensagem": f"Pedido de itens com id {id} deletado com sucesso"}