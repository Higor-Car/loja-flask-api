import pytest
from flask_jwt_extended import create_access_token, decode_token

from app.models import loja_db
from app.routes import auth, clientes, itensPedidos, pedidos
from tests.conftest import CLIENTE_LOGADO

ROTAS_PRIVADAS = [
    "/cliente",
    "/cliente/1",
    "/pedidos",
    "/pedidos/1",
    "/itensPedidos",
    "/itensPedidos/1",
]
CLIENTE_VALIDO = {"nome": "Bia", "email": "bia@example.com", "senha": "nova-senha"}
ITEM_VALIDO = {"pedido_id": 5, "produto_id": 1, "quantidade": 1}


def proibido(*_argumentos):
    raise AssertionError("Esta operação não deveria ser executada")


@pytest.mark.parametrize("rota", ROTAS_PRIVADAS)
def test_rotas_privadas_exigem_login(cliente_http, rota):
    assert cliente_http.get(rota).status_code == 401


def test_login_gera_token_com_o_id_do_cliente(aplicacao, cliente_http, monkeypatch):
    monkeypatch.setattr(auth, "buscarClientePorEmail", lambda email, senha: CLIENTE_LOGADO)

    resposta = cliente_http.post("/login", json={"email": "ana@example.com", "senha": "x"})

    with aplicacao.app_context():
        assert decode_token(resposta.get_json()["token"])["sub"] == "1"


def test_token_de_cliente_removido_e_recusado(aplicacao, cliente_http, monkeypatch, cabecalho_auth):
    monkeypatch.setattr(loja_db, "buscarUmCliente", lambda id: None)

    assert cliente_http.get("/cliente", headers=cabecalho_auth).status_code == 401


def test_token_antigo_com_email_e_recusado(aplicacao, cliente_http):
    with aplicacao.app_context():
        token = create_access_token(identity="ana@example.com")

    resposta = cliente_http.get("/cliente", headers={"Authorization": f"Bearer {token}"})

    assert resposta.status_code == 401


def test_lista_de_clientes_mostra_apenas_o_proprio(cliente_http, cabecalho_auth):
    resposta = cliente_http.get("/cliente", headers=cabecalho_auth)

    assert resposta.status_code == 200
    assert resposta.get_json() == [{"id": 1, "nome": "Ana", "email": "ana@example.com"}]


def test_cliente_nao_acessa_outro_cliente(cliente_http, cabecalho_auth, monkeypatch):
    monkeypatch.setattr(clientes, "atualizarCliente", proibido)
    monkeypatch.setattr(clientes, "deletarCliente", proibido)

    assert cliente_http.get("/cliente/2", headers=cabecalho_auth).status_code == 404
    assert cliente_http.put("/cliente/2", json=CLIENTE_VALIDO, headers=cabecalho_auth).status_code == 404
    assert cliente_http.delete("/cliente/2", headers=cabecalho_auth).status_code == 404


def test_cliente_atualiza_os_proprios_dados(cliente_http, cabecalho_auth, monkeypatch):
    chamadas = []
    monkeypatch.setattr(clientes, "atualizarCliente", lambda *dados: chamadas.append(dados))

    resposta = cliente_http.put("/cliente/1", json=CLIENTE_VALIDO, headers=cabecalho_auth)

    assert resposta.status_code == 200
    assert chamadas == [("Bia", "bia@example.com", "nova-senha", 1)]


def test_lista_apenas_pedidos_do_cliente_logado(cliente_http, cabecalho_auth, monkeypatch):
    pedido = {"id": 5, "cliente_id": 1, "data": "2026-11-18"}
    monkeypatch.setattr(pedidos, "buscarPedidosDoCliente", lambda cliente_id: [pedido] if cliente_id == 1 else [])

    assert cliente_http.get("/pedidos", headers=cabecalho_auth).get_json() == [pedido]


def test_novo_pedido_ignora_cliente_id_do_corpo(cliente_http, cabecalho_auth, monkeypatch):
    chamadas = []

    def inserir_falso(cliente_id, data):
        chamadas.append((cliente_id, data))
        return 5

    monkeypatch.setattr(pedidos, "inserirPedido", inserir_falso)

    resposta = cliente_http.post(
        "/pedidos", json={"cliente_id": 2, "data": "2026-11-18"}, headers=cabecalho_auth
    )

    assert resposta.status_code == 201
    assert resposta.get_json()["cliente_id"] == 1
    assert chamadas == [(1, "2026-11-18")]


def test_cliente_nao_acessa_pedido_de_outro(cliente_http, cabecalho_auth, monkeypatch):
    consultas = []

    def buscar_falso(id, cliente_id):
        consultas.append((id, cliente_id))
        return None

    monkeypatch.setattr(pedidos, "buscarPedidoDoCliente", buscar_falso)
    monkeypatch.setattr(pedidos, "atualizarPedido", proibido)
    monkeypatch.setattr(pedidos, "deletarPedido", proibido)
    corpo = {"data": "2026-11-19"}

    assert cliente_http.get("/pedidos/5", headers=cabecalho_auth).status_code == 404
    assert cliente_http.put("/pedidos/5", json=corpo, headers=cabecalho_auth).status_code == 404
    assert cliente_http.delete("/pedidos/5", headers=cabecalho_auth).status_code == 404
    assert consultas == [(5, 1), (5, 1), (5, 1)]


def test_lista_apenas_itens_do_cliente_logado(cliente_http, cabecalho_auth, monkeypatch):
    item = {"id": 9, **ITEM_VALIDO}
    monkeypatch.setattr(itensPedidos, "buscarItensDoCliente", lambda cliente_id: [item] if cliente_id == 1 else [])

    assert cliente_http.get("/itensPedidos", headers=cabecalho_auth).get_json() == [item]


def test_nao_adiciona_item_em_pedido_de_outro(cliente_http, cabecalho_auth, monkeypatch):
    monkeypatch.setattr(itensPedidos, "buscarPedidoDoCliente", lambda id, cliente_id: None)
    monkeypatch.setattr(itensPedidos, "inserirItensPedido", proibido)

    resposta = cliente_http.post("/itensPedidos", json=ITEM_VALIDO, headers=cabecalho_auth)

    assert resposta.status_code == 404


def test_cliente_nao_acessa_item_de_outro(cliente_http, cabecalho_auth, monkeypatch):
    monkeypatch.setattr(itensPedidos, "buscarItemDoCliente", lambda id, cliente_id: None)
    monkeypatch.setattr(itensPedidos, "atualizarItensPedido", proibido)
    monkeypatch.setattr(itensPedidos, "deletarItensPedidos", proibido)

    assert cliente_http.get("/itensPedidos/9", headers=cabecalho_auth).status_code == 404
    assert cliente_http.put("/itensPedidos/9", json=ITEM_VALIDO, headers=cabecalho_auth).status_code == 404
    assert cliente_http.delete("/itensPedidos/9", headers=cabecalho_auth).status_code == 404


def test_nao_move_item_para_pedido_de_outro(cliente_http, cabecalho_auth, monkeypatch):
    monkeypatch.setattr(itensPedidos, "buscarItemDoCliente", lambda id, cliente_id: {"id": id})
    monkeypatch.setattr(itensPedidos, "buscarPedidoDoCliente", lambda id, cliente_id: None)
    monkeypatch.setattr(itensPedidos, "atualizarItensPedido", proibido)

    resposta = cliente_http.put("/itensPedidos/9", json=ITEM_VALIDO, headers=cabecalho_auth)

    assert resposta.status_code == 404
