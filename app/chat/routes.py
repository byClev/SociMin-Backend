from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.chat.services import chat_service
from app.chat.schemas import (
    CreateChatSchema, ChatSchema,
    CreateMessageSchema, MessageSchema
)
from app.chat.exceptions import (
    ChatNotFound, UnauthorizedAccess,
    ChatAlreadyExists
)

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


# ── Chats ───────────────────────────────────────────────

@chat_bp.post("/")
@jwt_required()
def create_chat():
    data    = CreateChatSchema().load(request.json)
    user_id = get_jwt_identity()
    chat    = chat_service.create_chat(
        user_id_1 = user_id,
        user_id_2 = data["user_id_2"]
    )
    return jsonify(ChatSchema().dump(chat)), 201


@chat_bp.get("/")
@jwt_required()
def list_chats():
    user_id  = get_jwt_identity()
    page     = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    pagination = chat_service.get_chats(user_id, page=page, per_page=per_page)

    return jsonify({
        "items":    ChatSchema(many=True).dump(pagination.items),
        "total":    pagination.total,
        "pages":    pagination.pages,
        "has_next": pagination.has_next
    }), 200


# ── Messages ────────────────────────────────────────────

@chat_bp.post("/<int:chat_id>/messages")
@jwt_required()
def send_message(chat_id):
    data    = CreateMessageSchema().load(request.json)
    user_id = int(get_jwt_identity())

    message = chat_service.send_message(
        chat_id   = chat_id,
        sender_id = user_id,
        content   = data["content"]
    )
    return jsonify(MessageSchema().dump(message)), 201


@chat_bp.get("/<int:chat_id>/messages")
@jwt_required()
def get_messages(chat_id):
    user_id  = int(get_jwt_identity())
    after_id = request.args.get("after", type=int)
    page     = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    pagination = chat_service.get_messages(
        chat_id  = chat_id,
        user_id  = user_id,
        after_id = after_id,
        page     = page,
        per_page = per_page
    )

    return jsonify({
        "items":    MessageSchema(many=True).dump(pagination.items),
        "total":    pagination.total,
        "pages":    pagination.pages,
        "has_next": pagination.has_next
    }), 200


@chat_bp.patch("/<int:chat_id>/read")
@jwt_required()
def mark_as_read(chat_id):
    chat_service.mark_as_read(chat_id, get_jwt_identity())
    return jsonify({"message": "Mensagens marcadas como lidas"}), 200


# ── Error handlers ──────────────────────────────────────

@chat_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({"error": e.messages}), 422

@chat_bp.errorhandler(ChatNotFound)
def handle_not_found(e):
    return jsonify({"error": "Chat não encontrado"}), 404

@chat_bp.errorhandler(UnauthorizedAccess)
def handle_unauthorized(e):
    return jsonify({"error": "Acesso não autorizado"}), 403

@chat_bp.errorhandler(ChatAlreadyExists)
def handle_already_exists(e):
    return jsonify({"error": "Chat já existe"}), 409