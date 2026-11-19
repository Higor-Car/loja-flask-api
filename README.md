# Loja Flask API

API REST desenvolvida em Python com Flask para gerenciar produtos, clientes, pedidos e itens de pedido, com autenticação JWT, documentação Swagger e um endpoint de perguntas em linguagem natural que usa a API da Anthropic (Claude) para consultar os produtos.

> **Status do deploy:** a instância AWS EC2 que hospedava esta API foi desativada em novembro de 2026 e o endereço público não existe mais. O projeto continua disponível para execução local. Os detalhes de como o deploy funcionava estão em [Histórico de deploy](#histórico-de-deploy-desativado).

## Tecnologias

- **Python 3.11**
- **Flask 3.1** + **flask-smorest** (organização de blueprints e documentação OpenAPI/Swagger automática)
- **Flask-JWT-Extended** — autenticação via token JWT
- **bcrypt** — hash seguro de senhas
- **flask-cors** — liberação de CORS para consumo por front-ends externos
- **marshmallow** — validação e serialização de dados via schemas
- **PostgreSQL** (via **psycopg2**) — banco de dados
- **python-dotenv** — configuração por variáveis de ambiente
- **Anthropic API (Claude)** — agente com *tool use* para responder perguntas sobre os produtos
- **Gunicorn** — servidor WSGI de produção

## Estrutura principal

| Caminho | Função |
|---|---|
| `app.py` | Ponto de entrada da aplicação (`create_app()`) |
| `app/__init__.py` | Fábrica da aplicação: configuração, JWT, CORS e registro dos blueprints |
| `app/routes/` | Rotas por recurso: `auth`, `produtos`, `clientes`, `pedidos`, `itensPedidos` e `perguntar` |
| `app/models/loja_db.py` | Camada de acesso ao banco de dados |
| `app/models/schema.py` | Conexão com o PostgreSQL e criação das tabelas |
| `app/schemas/` | Schemas de validação/serialização (marshmallow) |
| `app/services/` | Agente de IA (`agente.py`) e as ferramentas que ele pode chamar (`tools.py`, `tools_schema.py`) |
| `tests/` | Pasta de testes |
| `Procfile` | Comando de start em produção (`gunicorn app:app`) |
| `runtime.txt` | Versão do Python |
| `requirements.txt` | Dependências do projeto |
| `.github/workflows/deploy.yml` | Pipeline de deploy via GitHub Actions (desativado, execução apenas manual) |

## Como executar localmente

Pré-requisito: um servidor PostgreSQL acessível.

```bash
git clone https://github.com/Higor-Car/loja-flask-api.git
cd loja-flask-api
python -m venv venv
source venv/bin/activate      # no Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto:

```env
JWT_SECRET_KEY=troque_por_uma_chave_secreta
DB_HOST=localhost
DB_PORT=5432
DB_USER=seu_usuario
DB_NAME=nome_do_banco
DB_PASSWORD=sua_senha
ANTHROPIC_API_KEY=sua_chave_da_anthropic   # necessária apenas para o endpoint /perguntar
```

Inicie o servidor:

```bash
python app.py
```

As tabelas são criadas automaticamente (`CREATE TABLE IF NOT EXISTS`) por `app/models/schema.py`. O servidor fica disponível em `http://localhost:5000`, com a documentação Swagger em `http://localhost:5000/docs`.

## Autenticação

As rotas de escrita (`POST`, `PUT` e `DELETE`) e o endpoint `/perguntar` exigem um token JWT válido, obtido em `/login`. As rotas de leitura (`GET`) são públicas. Envie o token no header:

```
Authorization: Bearer <seu_token>
```

## Rotas principais

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|--------------|
| POST | `/login` | Autenticar e obter token JWT | Não |
| GET | `/produtos` | Listar produtos | Não |
| POST | `/produtos` | Criar produto | Sim |
| GET | `/produtos/<id>` | Buscar produto | Não |
| PUT/DELETE | `/produtos/<id>` | Atualizar / Deletar produto | Sim |
| GET | `/cliente` | Listar clientes | Não |
| POST | `/cliente` | Criar cliente | Sim |
| GET | `/cliente/<id>` | Buscar cliente | Não |
| PUT/DELETE | `/cliente/<id>` | Atualizar / Deletar cliente | Sim |
| GET | `/pedidos` | Listar pedidos | Não |
| POST | `/pedidos` | Criar pedido | Sim |
| GET | `/pedidos/<id>` | Buscar pedido | Não |
| PUT/DELETE | `/pedidos/<id>` | Atualizar / Deletar pedido | Sim |
| GET | `/itensPedidos` | Listar itens de pedido | Não |
| POST | `/itensPedidos` | Criar item de pedido | Sim |
| GET | `/itensPedidos/<id>` | Buscar item de pedido | Não |
| PUT/DELETE | `/itensPedidos/<id>` | Atualizar / Deletar item de pedido | Sim |
| POST | `/perguntar` | Fazer uma pergunta em linguagem natural sobre os produtos | Sim |

> Lista completa e testável de todos os endpoints disponível no Swagger em `/docs` (rodando localmente).

### Endpoint `/perguntar`

Recebe uma pergunta em texto e devolve a resposta gerada por um agente que usa a API da Anthropic (Claude) com *tool use* para consultar os produtos cadastrados.

```json
// POST /perguntar
{ "pergunta": "Vocês têm algum produto com 'café' no nome?" }

// resposta
{ "resposta": "..." }
```

## Histórico de deploy (desativado)

Durante um período, a API ficou publicada em uma instância **AWS EC2** (Amazon Linux), servida via **Gunicorn** e gerenciada como serviço pelo **systemd**, com reinício automático em caso de falha, Elastic IP fixo e Security Group liberando as portas necessárias (API e SSH). Essa infraestrutura foi encerrada em novembro de 2026 para evitar custos, já que a API deixou de ser usada em produção.

### Deploy automático (CI/CD)

O deploy era automatizado via **GitHub Actions**. O pipeline definido em [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) executava, a cada `push` na branch `main`:

1. Checkout do código
2. Conexão SSH com o servidor EC2 (usando uma chave privada armazenada em **GitHub Secrets**, nunca exposta no código)
3. `git pull` e instalação das dependências no servidor
4. Reinício do serviço (`systemctl restart loja-flask`) para aplicar as mudanças

O workflow foi mantido no repositório como referência, mas agora só roda manualmente (`workflow_dispatch`), pois o servidor de destino não existe mais.

## Próximos passos

- Adicionar testes automatizados com `pytest` e uma etapa de **CI** que os execute a cada push.

## Autor

Desenvolvido por [Higor Cardoso Alves de Faria](https://github.com/Higor-Car).
