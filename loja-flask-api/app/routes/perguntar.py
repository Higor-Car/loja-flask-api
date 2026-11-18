from flask_smorest import Blueprint,abort
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from app.services.agente import processarPergunta
from app.schemas.schemas import PerguntaSchema,RespostaSchema

blp = Blueprint("perguntar", __name__, description="Perguntas do usúario")

@blp.route("/perguntar")
class Perguntar(MethodView):

    @jwt_required()
    @blp.arguments(PerguntaSchema)
    @blp.response(200, RespostaSchema)
    def post(self, dados):
        pergunta = dados["pergunta"]
        try:
            texto = processarPergunta(pergunta)
        except:
            abort(503, message="Service Unavaiable")
        return {"resposta": texto}