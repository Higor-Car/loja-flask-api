from marshmallow import Schema, fields

class ProdutoSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    preco = fields.Float(required=True)
    descricao = fields.Str()
    quantidade = fields.Int(required=True)

class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    email = fields.Email(required=True)
    senha = fields.Str(required=True, load_only=True)

class PedidoSchema(Schema):
    id = fields.Int(dump_only=True)
    cliente_id = fields.Int(required=True)
    data = fields.Str(required=True)

class ItensPedidoSchema(Schema):
    id = fields.Int(dump_only=True)
    pedido_id = fields.Int(required=True)
    produto_id = fields.Int(required=True)
    quantidade = fields.Int(required=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    senha = fields.Str(required=True)