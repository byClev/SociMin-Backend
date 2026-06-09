from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.profile.services import profile_service
from app.profile.schemas import createProfileSchema, updateProfileSchema, addContactSchema, ProfileSchema, ContactSchema

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

@profile_bp.post("/create")
@jwt_required()
def create_profile():
    user_id = get_jwt_identity()
    data = createProfileSchema().load(request.json)
    profile = profile_service.create_profile(
        user_id=user_id,
        nickname=data["nickname"],
        bio=data.get("bio"),
        avatar_id=data.get("avatar_id")
    )
    return jsonify(ProfileSchema().dump(profile)), 201

@profile_bp.get("/me")
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    profile = profile_service.get_profile_by_user_id(user_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404
    return jsonify(ProfileSchema().dump(profile)), 200

@profile_bp.put("/update")
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = updateProfileSchema().load(request.json)
    try:
        profile = profile_service.update_profile(
            user_id=user_id,
            nickname=data.get("nickname"),
            bio=data.get("bio"),
            avatar_id=data.get("avatar_id")
        )
        return jsonify(ProfileSchema().dump(profile)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@profile_bp.delete("/delete")
@jwt_required()
def delete_profile():
    user_id = get_jwt_identity()
    try:
        profile_service.delete_profile(user_id=user_id, profile_id=user_id)
        return jsonify({"message": "Profile deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@profile_bp.post("/contacts")
@jwt_required()
def add_contact():
    user_id = get_jwt_identity()
    data = addContactSchema().load(request.json)
    try:
        contact = profile_service.add_contact(
            user_id=user_id,
            profile_id=data["profile_id"],
            contact_profile_id=data["contact_profile_id"]
        )
        return jsonify(ContactSchema().dump(contact)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@profile_bp.get("/contacts")
@jwt_required() #verificar se é necessário proteger essa rota, já que ela depende do profile_id e não do user_id
def get_contacts():
    user_id = get_jwt_identity()
    profile = profile_service.get_profile_by_user_id(user_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404
    contacts = profile_service.get_contacts(profile.id)
    return jsonify([ProfileSchema().dump(contact) for contact in contacts]), 200

@profile_bp.delete("/contacts")
@jwt_required()
def remove_contact():
    user_id = get_jwt_identity()
    data = addContactSchema().load(request.json)
    try:
        profile_service.remove_contact(
            user_id=user_id,
            profile_id=data["profile_id"],
            contact_profile_id=data["contact_profile_id"]
        )
        return jsonify({"message": "Contact removed successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
