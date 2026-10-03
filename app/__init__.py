from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.routes.produtos import blp as ProdutosBlp
from app.routes.clientes import blp as ClientesBlp
from app.routes.pedidos import blp as PedidosBlp
from app.routes.itensPedidos import blp as ItensPedidosBlp
from app.routes.auth import blp as AuthBlp
from app.routes.perguntar import blp as PerguntarBlp


def create_app():
    app = Flask(__name__)
    load_dotenv()

    CORS(app)
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
    app.config["API_TITLE"] = "Loja API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    JWTManager(app)
    api = Api(app)

    api.register_blueprint(ProdutosBlp)
    api.register_blueprint(ClientesBlp)
    api.register_blueprint(PedidosBlp)
    api.register_blueprint(ItensPedidosBlp)
    api.register_blueprint(AuthBlp)
    api.register_blueprint(PerguntarBlp)

    return app