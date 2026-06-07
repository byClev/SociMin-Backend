from flask_jwt_extended import jwt_required, get_jwt_identity
from app.blog.schemas import CreateBlogPostSchema, BlogPostSchema
from flask import Blueprint, jsonify, request
from app.blog.services import blog_service

blog_bp = Blueprint("blog", __name__, url_prefix="/blog")

@blog_bp.post("/post")
@jwt_required()
def create_post():
    data = CreateBlogPostSchema().load(request.json)
    author_id = int(get_jwt_identity())

    post = blog_service.create_post(
        title=data["title"],
        content=data["content"],
        author_id=author_id,
        image_id=data.get("image_id")
    )

    return jsonify(BlogPostSchema().dump(post)), 201

@blog_bp.get("/post/<int:post_id>")
def get_post(post_id):
    post = blog_service.get_post_by_id(post_id)
    if not post:
        return jsonify({"message": "Post not found"}), 404
    return jsonify(BlogPostSchema().dump(post)), 200

@blog_bp.get("/posts")
def get_posts():
    posts = blog_service.get_all_posts()
    return jsonify(BlogPostSchema(many=True).dump(posts)), 200

@blog_bp.get("/posts/author/<int:author_id>")
def get_posts_by_author(author_id):
    posts = blog_service.get_posts_by_author(author_id)
    return jsonify(BlogPostSchema(many=True).dump(posts)), 200

@blog_bp.put("/post/<int:post_id>")
@jwt_required()
def update_post(post_id):
    data = CreateBlogPostSchema().load(request.json)
    post = blog_service.update_post(
        post_id=post_id,
        title=data.get("title"),
        content=data.get("content"),
        image_id=data.get("image_id")
    )
    if not post:
        return jsonify({"message": "Post not found"}), 404
    return jsonify(BlogPostSchema().dump(post)), 200

@blog_bp.delete("/post/<int:post_id>")
@jwt_required()
def delete_post(post_id):
    author_id = int(get_jwt_identity())
    success = blog_service.delete_post(post_id, author_id)
    if not success:
        return jsonify({"message": "Post not found"}), 404
    return jsonify({"message": "Post deleted successfully"}), 200