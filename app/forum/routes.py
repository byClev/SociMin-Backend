from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.forum.services import forum_service
from app.forum.schemas import (
    CreateForumSchema,
    CreatePostSchema,
    CreateCommentSchema,
    ForumSchema, 
    ForumPostSchema, 
    ForumCommentSchema,
    UpdateCommentSchema,
    UpdateForumSchema,
    UpdatePostSchema
    )

forum_bp = Blueprint("forum", __name__, url_prefix="/forum")

# Forum routes ------------------------------------------------------------------------------------------

@forum_bp.post("/")
@jwt_required()
def create_forum():
    data = CreateForumSchema().load(request.json)
    forum = forum_service.create_forum(
        title=data["title"],
        description=data.get("description", ""),
        user_id=get_jwt_identity()
    )
    return jsonify(ForumSchema().dump(forum)), 201

@forum_bp.get("/<int:forum_id>")
def get_forum(forum_id):
    forum = forum_service.get_forum_by_id(forum_id)
    if not forum:
        return jsonify({"message": "Forum not found"}), 404
    return jsonify(ForumSchema().dump(forum)), 200

@forum_bp.get("/") #pega todos os forums, ou os forums de um usuario se user_id for passado como query param
def list_forums():
    user_id  = request.args.get("user_id", type=int)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    forums = forum_service.get_forums(user_id=user_id, page=page, per_page=per_page)

    return jsonify({
        "forums": ForumSchema(many=True).dump(forums.items),
        "total": forums.total,
        "pages": forums.pages,
        "current_page": forums.page
    }), 200

@forum_bp.put("/<int:forum_id>")
@jwt_required()
def update_forum(forum_id):
    data = UpdateForumSchema().load(request.json)
    forum = forum_service.update_forum(
        forum_id=forum_id,
        title=data.get("title"),
        description=data.get("description")
    )
    if not forum:
        return jsonify({"message": "Forum not found"}), 404
    return jsonify(ForumSchema().dump(forum)), 200

@forum_bp.delete("/<int:forum_id>")
@jwt_required()
def delete_forum(forum_id):
    success = forum_service.delete_forum(forum_id, int(get_jwt_identity()))
    if not success:
        return jsonify({"message": "Forum not found"}), 404
    return jsonify({"message": "Forum deleted successfully"}), 200

# Post routes ------------------------------------------------------------------------------------------

@forum_bp.post("/<int:forum_id>/posts")
@jwt_required()
def create_post(forum_id):
    data = CreatePostSchema().load(request.json)
    post = forum_service.create_post(
        forum_id=forum_id,
        user_id=get_jwt_identity(),
        title=data["title"],
        content=data["content"],
        image_id=data.get("image_id")
    )
    return jsonify(ForumPostSchema().dump(post)), 201

@forum_bp.get("/posts/<int:post_id>") #pega um post pelo id
def get_post(post_id):
    post = forum_service.get_post_by_id(post_id)
    if not post:
        return jsonify({"message": "Post not found"}), 404
    return jsonify(ForumPostSchema().dump(post)), 200


@forum_bp.get("/posts")
def list_posts():
    forum_id = request.args.get("forum_id", type=int)
    user_id  = request.args.get("user_id", type=int)
    page     = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    posts = forum_service.get_posts_filtered( forum_id=forum_id, user_id=user_id, page=page, per_page=per_page)

    return jsonify({
        "posts": ForumPostSchema(many=True).dump(posts.items),
        "total": posts.total,
        "pages": posts.pages,
        "current_page": posts.page
    }), 200

@forum_bp.put("/posts/<int:post_id>")
@jwt_required()
def update_post(post_id):
    data = UpdatePostSchema().load(request.json)
    post = forum_service.update_post(
        post_id=post_id,
        user_id=int(get_jwt_identity()),
        title=data.get("title"),
        content=data.get("content"),
        image_id=data.get("image_id")
    )
    if not post:
        return jsonify({"message": "Post not found"}), 404
    return jsonify(ForumPostSchema().dump(post)), 200

@forum_bp.delete("/posts/<int:post_id>")
@jwt_required()
def delete_post(post_id):
    success = forum_service.delete_post(post_id, int(get_jwt_identity()))
    if not success:
        return jsonify({"message": "Post not found"}), 404
    return jsonify({"message": "Post deleted successfully"}), 200

# Comment routes ---------------------------------------------------------------------------------------

@forum_bp.post("/posts/<int:post_id>/comments")
@jwt_required()
def create_comment(post_id):
    data = CreateCommentSchema().load(request.json)
    comment = forum_service.create_comment(
        post_id=post_id,
        user_id=int(get_jwt_identity()),
        content=data["content"]
    )
    return jsonify(ForumCommentSchema().dump(comment)), 201

@forum_bp.get("/posts/comments/<int:comment_id>")
def get_comment(comment_id):
    comment = forum_service.get_comment_by_id(comment_id)
    if not comment:
        return jsonify({"message": "Comment not found"}), 404
    return jsonify(ForumCommentSchema().dump(comment)), 200

@forum_bp.get("/posts/comments")
def list_comments():
    post_id  = request.args.get("post_id", type=int)
    user_id  = request.args.get("user_id", type=int)
    page     = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    comments = forum_service.get_comments_filtered(post_id=post_id, user_id=user_id, page=page, per_page=per_page)

    return jsonify({
        "comments": ForumCommentSchema(many=True).dump(comments.items),
        "total": comments.total,
        "pages": comments.pages,
        "current_page": comments.page
    }), 200

@forum_bp.put("/posts/comments/<int:comment_id>")
@jwt_required()
def update_comment(comment_id):
    data = UpdateCommentSchema().load(request.json)
    comment = forum_service.update_comment(
        comment_id=comment_id,
        user_id=int(get_jwt_identity()),
        content=data["content"]
    )
    if not comment:
        return jsonify({"message": "Comment not found"}), 404
    return jsonify(ForumCommentSchema().dump(comment)), 200

@forum_bp.delete("/posts/comments/<int:comment_id>")
@jwt_required()
def delete_comment(comment_id):
    success = forum_service.delete_comment(comment_id, int(get_jwt_identity()))
    if not success:
        return jsonify({"message": "Comment not found"}), 404
    return jsonify({"message": "Comment deleted successfully"}), 200