from datetime import date
from app.models import loja_db

def buscar_produto(nome: str) -> dict:
    try:
        todos = loja_db.buscarTodosOsProdutos()
        nome_lower = nome.lower()
        encontrados = [p for p in todos if nome_lower in p["nome"].lower()]

        if not encontrados:
            return {"sucesso": False, "dados": None, "mensagem": f"Nenhum produto encontrado para '{nome}'"}
        return {"sucesso": True, "dados": encontrados, "mensagem": f"{len(encontrados)} produto(s) encontrado(s)"}
    except Exception as e:
        return {"sucesso": False, "dados": None, "mensagem": f"Erro ao buscar produto: {str(e)}"}


def criar_pedido(cliente_id: int, itens: list) -> dict:
    try:
        pedido_id = loja_db.criarPedidoCompleto(cliente_id, str(date.today()), itens)
        return {
            "sucesso": True,
            "dados": {"pedido_id": pedido_id, "itens": itens},
            "mensagem": "Pedido criado com sucesso"
        }
    except ValueError as e:
        return {"sucesso": False, "dados": None, "mensagem": str(e)}
    except Exception as e:
        return {"sucesso": False, "dados": None, "mensagem": f"Erro ao criar pedido: {str(e)}"}


TOOL_FUNCTIONS = {
    "buscar_produto": buscar_produto,
    "criar_pedido": criar_pedido,
}