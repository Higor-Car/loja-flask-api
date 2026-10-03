import os
from dotenv import load_dotenv
import anthropic
from app.services.tools_schema import TOOLS
from app.services.tools import TOOL_FUNCTIONS
import json

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODEL = "claude-sonnet-4-5"


def processarPergunta(perguntaUsuario: str) -> str:
    messages = [
        {"role": "user", "content": perguntaUsuario}
    ]

    response = client.messages.create(model=MODEL, max_tokens=1024, messages=messages, tools=TOOLS)

    while response.stop_reason == "tool_use":

        blocos_tool = [p for p in response.content if p.type == "tool_use"]
        blocosResultado = []
        for i in blocos_tool:
            tool_func = TOOL_FUNCTIONS[i.name]
            resultado = tool_func(**i.input)
            blocosResultado.append({
                "type": "tool_result",
                "tool_use_id": i.id,
                "content": json.dumps(resultado)
            })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": blocosResultado})

        response = client.messages.create(model=MODEL, max_tokens=1024, messages=messages, tools=TOOLS)

    blocosTexto = [p for p in response.content if p.type == "text"]

    respostaFinal = ""

    for i in blocosTexto:
        respostaFinal += i.text

    return respostaFinal
