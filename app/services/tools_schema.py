TOOLS = [
    {
        "name": "buscar_produto",
        "description": "Busca produtos no catálogo pelo nome ou parte do nome. Use quando o cliente perguntar sobre disponibilidade, preço ou detalhes de um produto.",
        "input_schema": {
            "type": "object",
            "properties": {
                "nome": {
                    "type": "string",
                    "description": "Nome ou parte do nome do produto a buscar"
                }
            },
            "required": ["nome"]
        }
    },
    {
        "name": "criar_pedido",
        "description": "Cria um novo pedido para um cliente com uma lista de itens. Use quando o cliente confirmar que quer fazer um pedido.",
        "input_schema": {
            "type": "object",
            "properties": {
                "cliente_id": {"type": "integer", "description": "ID do cliente"},
                "itens": {
                    "type": "array",
                    "description": "Lista de itens do pedido",
                    "items": {
                        "type": "object",
                        "properties": {
                            "produto_id": {"type": "integer"},
                            "quantidade": {"type": "integer"}
                        },
                        "required": ["produto_id", "quantidade"]
                    }
                }
            },
            "required": ["cliente_id", "itens"]
        }
    }
]