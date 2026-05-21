from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from routes.produtos import blp as ProdutosBlp
from routes.clientes import blp as ClientesBlp
from routes.pedidos import blp as PedidosBlp
from routes.itensPedidos import blp as ItensPedidosBlp
from routes.auth import blp as AuthBlp

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "kj#92@xLp!mQ3z"
app.config["API_TITLE"] = "Loja API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

jwt = JWTManager(app)
api = Api(app)

api.register_blueprint(ProdutosBlp)
api.register_blueprint(ClientesBlp)
api.register_blueprint(PedidosBlp)
api.register_blueprint(ItensPedidosBlp)
api.register_blueprint(AuthBlp)

if __name__ == "__main__":
    app.run(debug=True)