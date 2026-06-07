import os
from flask import Blueprint, current_app, request, jsonify, send_file
from flask_jwt_extended import jwt_required

from app.storage.services import storage_service
from werkzeug.exceptions import BadRequest, NotFound

storage_bp = Blueprint("storage", __name__, url_prefix="/storage")

@storage_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    if "file" not in request.files:
        raise BadRequest("file field is required")
    file = request.files["file"]
    svc = storage_service
    try:
        file_id = svc.save(file)
    except ValueError:
        raise BadRequest("invalid file type")
    return jsonify({"id": file_id}), 201

@storage_bp.route("/<file_id>", methods=["GET"])
def serve(file_id):
    svc = storage_service
    path = svc.path_for(file_id)

    if path is None:
        raise NotFound()
    
    return send_file(path, conditional=True)