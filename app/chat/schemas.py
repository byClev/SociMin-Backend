from marshmallow import Schema, fields, validate


class CreateChatSchema(Schema):
    user_id_2 = fields.Int(required=True)  # com quem quer conversar


class ChatSchema(Schema):
    id         = fields.Int(dump_only=True)
    user_id_1  = fields.Int(dump_only=True)
    user_id_2  = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class CreateMessageSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=1000))


class MessageSchema(Schema):
    id              = fields.Int(dump_only=True)
    chat_id         = fields.Int(dump_only=True)
    sender_id       = fields.Int(dump_only=True)
    content         = fields.Str(dump_only=True)
    read            = fields.Bool(dump_only=True)
    created_at      = fields.DateTime(dump_only=True)