# Loja Flask API

API REST desenvolvida em Python com Flask para gerenciar produtos, clientes, pedidos e itens de pedido, com autenticação JWT e documentação Swagger.

## Tecnologias

- **Python 3.11**
- **Flask 3.1** + **flask-smorest** (organização de blueprints e documentação OpenAPI/Swagger automática)
- **Flask-JWT-Extended** — autenticação via token JWT
- **bcrypt** — hash seguro de senhas
- **flask-cors** — liberação de CORS para consumo por front-ends externos
- **marshmallow** — validação e serialização de dados via schemas
- **SQLite3** — banco de dados
- **Gunicorn** — servidor WSGI de produção

## Estrutura principal

| Arquivo | Função |
|---|---|
| `app.py` | Ponto de entrada da aplicação, registro de blueprints |
| `schemas.py` | Schemas de validação/serialização (marshmallow) |
| `loja_db.py` | Camada de acesso ao banco de dados |
| `Banco.py` | Criação/inicialização das tabelas do SQLite |
| `Procfile` | Comando de start em produção (`gunicorn app:app`) |
| `runtime.txt` | Versão do Python usada em produção |
| `requirements.txt` | Dependências do projeto |

## Como executar localmente

```bash
git clone https://github.com/Higor-Car/loja-flask-api.git
cd loja-flask-api
pip install -r requirements.txt
python Banco.py      # cria/inicializa o banco SQLite
python app.py         # inicia o servidor
```

Servidor disponível em `http://127.0.0.1:5000`, com documentação Swagger em `http://127.0.0.1:5000/docs`.

## Autenticação

A maior parte das rotas exige um token JWT válido, obtido via login. Envie o token no header:

```
Authorization: Bearer <seu_token>
```

## Rotas principais

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|--------------|
| POST | `/auth/registrar` | Criar novo usuário | Não |
| POST | `/auth/login` | Autenticar e obter token JWT | Não |
| GET/POST | `/produtos` | Listar / Criar produto | Sim |
| GET/PUT/DELETE | `/produtos/<id>` | Buscar / Atualizar / Deletar produto | Sim |
| GET/POST | `/clientes` | Listar / Criar cliente | Sim |
| GET/PUT/DELETE | `/clientes/<id>` | Buscar / Atualizar / Deletar cliente | Sim |
| GET/POST | `/pedidos` | Listar / Criar pedido | Sim |
| GET/PUT/DELETE | `/pedidos/<id>` | Buscar / Atualizar / Deletar pedido | Sim |
| GET/POST | `/itensPedidos` | Listar / Criar item de pedido | Sim |
| GET/PUT/DELETE | `/itensPedidos/<id>` | Buscar / Atualizar / Deletar item de pedido | Sim |

> Lista completa e testável de todos os 20 endpoints disponível no Swagger em `/docs` (rodando localmente).

## Autor

Desenvolvido por [Higor Cardoso Alves de Faria](https://github.com/Higor-Car).
