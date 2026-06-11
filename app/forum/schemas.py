from marshmallow import Schema, fields, validate

#Forum Schemas------------------------------------------
class CreateForumSchema(Schema):
    title       = fields.Str(required=True, validate=validate.Length(min=3, max=64))
    description = fields.Str(validate=validate.Length(max=500))

class UpdateForumSchema(Schema):
    title       = fields.Str(validate=validate.Length(min=3, max=64))
    description = fields.Str(validate=validate.Length(max=500))

class ForumSchema(Schema):
    id          = fields.Int(dump_only=True)
    user_id     = fields.Int(dump_only=True)
    title       = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    created_at  = fields.DateTime(dump_only=True)
    updated_at  = fields.DateTime(dump_only=True)

#Post Schemas-------------------------------------------
class CreatePostSchema(Schema):
    title    = fields.Str(required=True, validate=validate.Length(min=1, max=32))
    content  = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    image_id = fields.Str(validate=validate.Length(max=32))
    video_url = fields.Str(validate=validate.Length(max=255))

class UpdatePostSchema(Schema):
    title    = fields.Str(validate=validate.Length(min=1, max=32))
    content  = fields.Str(validate=validate.Length(min=1, max=500))
    image_id = fields.Str(validate=validate.Length(max=32))
    video_url = fields.Str(validate=validate.Length(max=255))

class ForumPostSchema(Schema):
    id         = fields.Int(dump_only=True)
    forum_id   = fields.Int(dump_only=True)
    user_id    = fields.Int(dump_only=True)
    title      = fields.Str(dump_only=True)
    content    = fields.Str(dump_only=True)
    image_id   = fields.Str(dump_only=True)
    video_url  = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

#Comment Schemas------------------------------------------
class CreateCommentSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=300))

class UpdateCommentSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=300))

class ForumCommentSchema(Schema):
    id         = fields.Int(dump_only=True)
    post_id    = fields.Int(dump_only=True)
    user_id    = fields.Int(dump_only=True)
    content    = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)