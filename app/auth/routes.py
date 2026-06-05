from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.auth.services import auth_service
from app.auth.schemas import RegisterSchema, LoginSchema, UserSchema
from app.auth.exceptions import (
    EmailAlreadyExists,
    UsernameAlreadyExists,
    InvalidCredentials,
    InactiveUser
)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    data = RegisterSchema().load(request.json)
    user = auth_service.create_user(**data)
    return jsonify(UserSchema().dump(user)), 201


@auth_bp.post("/login")
def login():
    data = LoginSchema().load(request.json)
    user = auth_service.authenticate(**data)

    access_token  = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "access_token":  access_token,
        "refresh_token": refresh_token,
        "user": UserSchema().dump(user)
    }), 200


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id      = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": access_token}), 200


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user    = auth_service.get_user_by_id(user_id)
    return jsonify(UserSchema().dump(user)), 200


# ── Error handlers ─────────────────────────────────────

@auth_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({"error": e.messages}), 422

@auth_bp.errorhandler(EmailAlreadyExists)
def handle_email_exists(e):
    return jsonify({"error": "Email já cadastrado"}), 409

@auth_bp.errorhandler(UsernameAlreadyExists)
def handle_username_exists(e):
    return jsonify({"error": "Username já cadastrado"}), 409

@auth_bp.errorhandler(InvalidCredentials)
def handle_invalid_credentials(e):
    return jsonify({"error": "Credenciais inválidas"}), 401

@auth_bp.errorhandler(InactiveUser)
def handle_inactive_user(e):
    return jsonify({"error": "Usuário inativo"}), 403