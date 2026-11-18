import pytest

from app.models import loja_db


@pytest.mark.parametrize("quantidade", [0, -5])
def test_recusa_quantidade_invalida_antes_de_acessar_o_banco(quantidade):
    with pytest.raises(ValueError, match="maior que zero"):
        loja_db.criarPedidoCompleto(1, "2026-11-18", [{"produto_id": 1, "quantidade": quantidade}])


def test_recusa_pedido_sem_itens_antes_de_acessar_o_banco():
    with pytest.raises(ValueError, match="ao menos um item"):
        loja_db.criarPedidoCompleto(1, "2026-11-18", [])
