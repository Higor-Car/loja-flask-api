from tests.claude_falso import resposta_final

PERGUNTA = {"pergunta": "Tem camisa?"}


def test_exige_login(cliente_http, usar_claude):
    claude = usar_claude(resposta_final("Não deveria ser usado"))

    resposta = cliente_http.post("/perguntar", json=PERGUNTA)

    assert resposta.status_code == 401
    assert claude.chamadas == []


def test_exige_o_campo_pergunta(cliente_http, cabecalho_auth):
    resposta = cliente_http.post("/perguntar", json={}, headers=cabecalho_auth)

    assert resposta.status_code == 422


def test_devolve_a_resposta_do_agente(cliente_http, cabecalho_auth, usar_claude):
    usar_claude(resposta_final("Temos sim."))

    resposta = cliente_http.post("/perguntar", json=PERGUNTA, headers=cabecalho_auth)

    assert resposta.status_code == 200
    assert resposta.get_json() == {"resposta": "Temos sim."}


def test_avisa_quando_o_assistente_nao_esta_configurado(cliente_http, cabecalho_auth, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY")

    resposta = cliente_http.post("/perguntar", json=PERGUNTA, headers=cabecalho_auth)

    assert resposta.status_code == 503
    assert resposta.get_json()["message"] == "O assistente não está configurado neste servidor"


def test_falha_do_claude_nao_expoe_detalhes(cliente_http, cabecalho_auth, usar_claude):
    usar_claude(RuntimeError("detalhe interno"))

    resposta = cliente_http.post("/perguntar", json=PERGUNTA, headers=cabecalho_auth)

    assert resposta.status_code == 503
    assert resposta.get_json()["message"] == "O assistente está indisponível no momento"
    assert "detalhe interno" not in resposta.get_data(as_text=True)
