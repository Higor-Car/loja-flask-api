from app.routes import produtos

SEM_DESCRICAO = {"nome": "Boné", "preco": 20.0, "quantidade": 1}


def test_cria_produto_sem_descricao(cliente_http, cabecalho_auth, monkeypatch):
    recebido = []

    def inserir_falso(nome, preco, descricao, quantidade):
        recebido.append((nome, preco, descricao, quantidade))
        return 10

    monkeypatch.setattr(produtos, "inserirProduto", inserir_falso)

    resposta = cliente_http.post("/produtos", json=SEM_DESCRICAO, headers=cabecalho_auth)

    assert resposta.status_code == 201
    assert resposta.get_json()["id"] == 10
    assert recebido == [("Boné", 20.0, None, 1)]


def test_atualiza_produto_sem_descricao(cliente_http, cabecalho_auth, monkeypatch):
    recebido = []

    def atualizar_falso(nome, preco, descricao, quantidade, id):
        recebido.append((nome, preco, descricao, quantidade, id))

    monkeypatch.setattr(produtos, "atualizarProduto", atualizar_falso)

    resposta = cliente_http.put("/produtos/3", json=SEM_DESCRICAO, headers=cabecalho_auth)

    assert resposta.status_code == 200
    assert recebido == [("Boné", 20.0, None, 1, 3)]
