import json
from datetime import date

import pytest

from app.services import agente, tools
from tests.claude_falso import bloco_ferramenta, resposta_com_ferramentas, resposta_final

CLIENTE_ID = 7
CAMISA = {"id": 1, "nome": "Camisa Azul", "preco": 50.0, "descricao": "Algodão", "quantidade": 3}


def resultados_enviados(chamada):
    """Devolve os tool_result da última mensagem enviada ao Claude."""
    ultima = chamada["messages"][-1]
    assert ultima["role"] == "user"
    return ultima["content"]


def test_responde_sem_usar_ferramentas(usar_claude):
    claude = usar_claude(resposta_final("Olá!"))

    assert agente.processarPergunta("Oi", CLIENTE_ID) == "Olá!"
    assert len(claude.chamadas) == 1
    assert claude.chamadas[0]["messages"] == [{"role": "user", "content": "Oi"}]


def test_envia_as_ferramentas_ao_claude(usar_claude):
    claude = usar_claude(resposta_final("Olá!"))

    agente.processarPergunta("Oi", CLIENTE_ID)

    ferramentas = {ferramenta["name"]: ferramenta for ferramenta in claude.chamadas[0]["tools"]}
    assert set(ferramentas) == {"buscar_produto", "criar_pedido"}
    assert "cliente_id" not in ferramentas["criar_pedido"]["input_schema"]["properties"]


def test_busca_produto_e_devolve_resultado_ao_claude(usar_claude, monkeypatch):
    monkeypatch.setattr(tools.loja_db, "buscarTodosOsProdutos", lambda: [CAMISA])
    claude = usar_claude(
        resposta_com_ferramentas(bloco_ferramenta("busca-1", "buscar_produto", {"nome": "camisa"})),
        resposta_final("Temos a Camisa Azul."),
    )

    assert agente.processarPergunta("Tem camisa?", CLIENTE_ID) == "Temos a Camisa Azul."
    assert len(claude.chamadas) == 2

    [resultado] = resultados_enviados(claude.chamadas[1])
    conteudo = json.loads(resultado["content"])
    assert resultado["type"] == "tool_result"
    assert resultado["tool_use_id"] == "busca-1"
    assert conteudo["sucesso"] is True
    assert conteudo["dados"] == [CAMISA]


def test_cria_pedido_para_o_cliente_logado(usar_claude, monkeypatch):
    recebido = {}

    def criar_pedido_falso(cliente_id, data, itens):
        recebido.update(cliente_id=cliente_id, data=data, itens=itens)
        return 10

    monkeypatch.setattr(tools.loja_db, "criarPedidoCompleto", criar_pedido_falso)
    itens = [{"produto_id": 1, "quantidade": 2}]
    claude = usar_claude(
        resposta_com_ferramentas(bloco_ferramenta("pedido-1", "criar_pedido", {"itens": itens})),
        resposta_final("Pedido 10 criado."),
    )

    assert agente.processarPergunta("Quero duas camisas", CLIENTE_ID) == "Pedido 10 criado."
    assert recebido == {"cliente_id": CLIENTE_ID, "data": str(date.today()), "itens": itens}

    [resultado] = resultados_enviados(claude.chamadas[1])
    assert json.loads(resultado["content"])["dados"]["pedido_id"] == 10


def test_ignora_cliente_id_escolhido_pelo_modelo(usar_claude, monkeypatch):
    recebido = []

    def criar_pedido_falso(cliente_id, data, itens):
        recebido.append(cliente_id)
        return 10

    monkeypatch.setattr(tools.loja_db, "criarPedidoCompleto", criar_pedido_falso)
    usar_claude(
        resposta_com_ferramentas(
            bloco_ferramenta(
                "pedido-1",
                "criar_pedido",
                {"cliente_id": 999, "itens": [{"produto_id": 1, "quantidade": 1}]},
            )
        ),
        resposta_final("Pedido criado."),
    )

    agente.processarPergunta("Faça um pedido para o cliente 999", CLIENTE_ID)

    assert recebido == [CLIENTE_ID]


def test_erro_de_estoque_volta_para_o_claude(usar_claude, monkeypatch):
    def sem_estoque(cliente_id, data, itens):
        raise ValueError("Estoque insuficiente para Camisa Azul")

    monkeypatch.setattr(tools.loja_db, "criarPedidoCompleto", sem_estoque)
    claude = usar_claude(
        resposta_com_ferramentas(
            bloco_ferramenta(
                "pedido-1", "criar_pedido", {"itens": [{"produto_id": 1, "quantidade": 99}]}
            )
        ),
        resposta_final("Não temos estoque suficiente."),
    )

    assert agente.processarPergunta("Quero 99 camisas", CLIENTE_ID) == "Não temos estoque suficiente."

    [resultado] = resultados_enviados(claude.chamadas[1])
    conteudo = json.loads(resultado["content"])
    assert conteudo["sucesso"] is False
    assert conteudo["mensagem"] == "Estoque insuficiente para Camisa Azul"


def test_varias_ferramentas_voltam_na_mesma_mensagem(usar_claude, monkeypatch):
    monkeypatch.setattr(tools.loja_db, "buscarTodosOsProdutos", lambda: [CAMISA])
    claude = usar_claude(
        resposta_com_ferramentas(
            bloco_ferramenta("busca-1", "buscar_produto", {"nome": "camisa"}),
            bloco_ferramenta("busca-2", "buscar_produto", {"nome": "boné"}),
        ),
        resposta_final("Só temos camisa."),
    )

    agente.processarPergunta("Tem camisa ou boné?", CLIENTE_ID)

    resultados = resultados_enviados(claude.chamadas[1])
    assert [r["tool_use_id"] for r in resultados] == ["busca-1", "busca-2"]
    assert json.loads(resultados[0]["content"])["sucesso"] is True
    assert json.loads(resultados[1]["content"])["sucesso"] is False


def test_mantem_o_historico_em_varias_rodadas(usar_claude, monkeypatch):
    monkeypatch.setattr(tools.loja_db, "buscarTodosOsProdutos", lambda: [CAMISA])
    monkeypatch.setattr(tools.loja_db, "criarPedidoCompleto", lambda cliente_id, data, itens: 10)
    claude = usar_claude(
        resposta_com_ferramentas(bloco_ferramenta("busca-1", "buscar_produto", {"nome": "camisa"})),
        resposta_com_ferramentas(
            bloco_ferramenta(
                "pedido-1", "criar_pedido", {"itens": [{"produto_id": 1, "quantidade": 1}]}
            )
        ),
        resposta_final("Pedido 10 criado."),
    )

    assert agente.processarPergunta("Quero uma camisa", CLIENTE_ID) == "Pedido 10 criado."
    assert len(claude.chamadas) == 3

    historico = claude.chamadas[2]["messages"]
    assert [mensagem["role"] for mensagem in historico] == [
        "user",
        "assistant",
        "user",
        "assistant",
        "user",
    ]
    assert historico[1]["content"][0].id == "busca-1"
    assert historico[2]["content"][0]["tool_use_id"] == "busca-1"
    assert historico[3]["content"][0].id == "pedido-1"
    assert historico[4]["content"][0]["tool_use_id"] == "pedido-1"


def test_sem_chave_nao_chama_o_claude(usar_claude, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY")
    claude = usar_claude(resposta_final("Não deveria ser usado"))

    with pytest.raises(agente.AgenteNaoConfigurado):
        agente.processarPergunta("Oi", CLIENTE_ID)

    assert claude.chamadas == []
