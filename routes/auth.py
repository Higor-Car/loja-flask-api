from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token
from loja_db import buscarClientePorEmail
from schemas import LoginSchema

blp = Blueprint("auth", __name__, description="Autenticação")

@blp.route("/login")
class Login(MethodView):

    @blp.arguments(LoginSchema)
    @blp.response(200)
    def post(self, dados):
        cliente = buscarClientePorEmail(dados["email"], dados["senha"])
        if cliente is None:
            from flask_smorest import abort
            abort(401, message="Email ou senha inválidos")
        token = create_access_token(identity=dados["email"])
        return {"token": token}