"""Simula o cliente da Anthropic para testar o agente sem chave e sem internet."""
import copy
from types import SimpleNamespace


def bloco_texto(texto):
    return SimpleNamespace(type="text", text=texto)


def bloco_ferramenta(id, nome, entrada):
    return SimpleNamespace(type="tool_use", id=id, name=nome, input=entrada)


def resposta_final(texto):
    return SimpleNamespace(stop_reason="end_turn", content=[bloco_texto(texto)])


def resposta_com_ferramentas(*blocos):
    return SimpleNamespace(stop_reason="tool_use", content=list(blocos))


class ClaudeFalso:
    """Devolve as respostas na ordem definida e guarda cada chamada recebida."""

    def __init__(self, respostas):
        self.respostas = list(respostas)
        self.chamadas = []
        self.messages = self

    def create(self, **parametros):
        self.chamadas.append(copy.deepcopy(parametros))
        resposta = self.respostas.pop(0)
        if isinstance(resposta, Exception):
            raise resposta
        return resposta
