from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from loja_db import buscarTodosOsProdutos, buscarUmProduto, inserirProduto, atualizarProduto, deletarProduto
from schemas import ProdutoSchema

blp = Blueprint("produtos", __name__, description="Operações de produtos")

@blp.route("/produtos")
class ProdutoLista(MethodView):

    @blp.response(200, ProdutoSchema(many=True))
    def get(self):
        return buscarTodosOsProdutos()

    @jwt_required()
    @blp.arguments(ProdutoSchema)
    @blp.response(201, ProdutoSchema)
    def post(self, dados):
        id = inserirProduto(dados["nome"], dados["preco"], dados["descricao"], dados["quantidade"])
        return {**dados, "id": id}


@blp.route("/produtos/<int:id>")
class Produto(MethodView):

    @blp.response(200, ProdutoSchema)
    def get(self, id):
        produto = buscarUmProduto(id)
        if not produto:
            abort(404, message="Produto não encontrado")
        return produto

    @jwt_required()
    @blp.arguments(ProdutoSchema)
    @blp.response(200, ProdutoSchema)
    def put(self, dados, id):
        atualizarProduto(dados["nome"], dados["preco"], dados["descricao"], dados["quantidade"], id)
        return {**dados, "id": id}

    @jwt_required()
    @blp.response(200)
    def delete(self, id):
        deletarProduto(id)
        return {"mensagem": f"Produto com id {id} deletado com sucesso"}