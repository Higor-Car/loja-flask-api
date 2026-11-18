import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from app.models import loja_db
from app.services import agente
from tests.claude_falso import ClaudeFalso


@pytest.fixture(autouse=True)
def ambiente_de_teste(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "chave-apenas-para-testes-com-32-bytes-ou-mais")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "valor-apenas-para-testes")

    def conexao_proibida():
        raise AssertionError("Os testes não podem acessar o banco real")

    monkeypatch.setattr(loja_db, "connect", conexao_proibida)


@pytest.fixture
def usar_claude(monkeypatch):
    def configurar(*respostas):
        claude = ClaudeFalso(respostas)
        monkeypatch.setattr(agente, "client", claude)
        return claude

    return configurar


@pytest.fixture
def aplicacao():
    return create_app()


@pytest.fixture
def cliente_http(aplicacao):
    return aplicacao.test_client()


@pytest.fixture
def cabecalho_auth(aplicacao):
    with aplicacao.app_context():
        token = create_access_token(identity="teste@example.com")
    return {"Authorization": f"Bearer {token}"}
