from marshmallow import Schema, fields, validate

class CreateBlogPostSchema(Schema):
    title       = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    content     = fields.Str(required=True,validate=validate.Length(max=300))
    image_id    = fields.Str(validate=validate.Length(max=32))
    video_url   = fields.Str(validate=validate.Length(max=255))

class BlogPostSchema(Schema):
    id          = fields.Int(dump_only=True)
    title       = fields.Str(dump_only=True)
    content     = fields.Str(dump_only=True)
    image_id    = fields.Str(dump_only=True)
    video_url   = fields.Str(dump_only=True)
    author_id   = fields.Int(dump_only=True)
    created_at  = fields.DateTime(dump_only=True)
    updated_at  = fields.DateTime(dump_only=True)
