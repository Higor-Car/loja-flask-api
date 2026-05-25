# Loja Flask API

API REST desenvolvida em Python com Flask e SQLite para gerenciar produtos, clientes, pedidos e itens de pedido.

## Tecnologias
- Python 3, Flask, SQLite3

## Como executar

```bash
pip install flask
python Banco.py
python app.py
```

Servidor disponível em `http://127.0.0.1:5000`

## Rotas

| Método | Rota | Descrição |
|--------|------|-----------|
| GET/POST | `/produtos` | Listar / Criar produto |
| GET/PUT/DELETE | `/produtos/<id>` | Buscar / Atualizar / Deletar produto |
| GET/POST | `/clientes` | Listar / Criar cliente |
| GET/PUT/DELETE | `/clientes/<id>` | Buscar / Atualizar / Deletar cliente |
| GET/POST | `/pedidos` | Listar / Criar pedido |
| GET/PUT/DELETE | `/pedidos/<id>` | Buscar / Atualizar / Deletar pedido |
| GET/POST | `/itensPedidos` | Listar / Criar item |
| GET/PUT/DELETE | `/itensPedidos/<id>` | Buscar / Atualizar / Deletar item |
