from marshmallow import Schema, fields, validate

class createProfileSchema(Schema):
    nickname = fields.Str(required=True, validate=validate.Length(min=1, max=32))
    bio = fields.Str(validate=validate.Length(max=500))
    avatar_id = fields.Str(validate=validate.Length(max=32))

class updateProfileSchema(Schema):
    nickname = fields.Str(validate=validate.Length(min=1, max=32))
    bio = fields.Str(validate=validate.Length(max=500))
    avatar_id = fields.Str(validate=validate.Length(max=32))

class addContactSchema(Schema):
    profile_id = fields.Int(required=True)
    contact_profile_id = fields.Int(required=True)

class ProfileSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    nickname = fields.Str()
    bio = fields.Str()
    avatar_id = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class ContactSchema(Schema):
    id = fields.Int()
    profile_id = fields.Int()
    contact_profile_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
