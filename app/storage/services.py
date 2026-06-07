import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from pathlib import Path

ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "webp"}

class StorageService:
    @property
    def upload_dir(self):
        path = Path(__file__).resolve().parent / "images"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _allowed(self, filename):
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        return ext in ALLOWED_EXT

    def save(self, file_storage):
        base = self.upload_dir
        filename = secure_filename(file_storage.filename or "")
        
        if not filename or not self._allowed(filename):
            raise ValueError("invalid file")

        file_id = uuid.uuid4().hex
        ext = filename.rsplit(".", 1)[-1].lower()
        out_name = f"{file_id}.{ext}"
        out_path = base / out_name
        file_storage.save(out_path)
        return file_id

    def path_for(self, file_id):
        base = self.upload_dir
        for name in os.listdir(base):
            if name.startswith(file_id):
                return base / name
        return None

storage_service = StorageService()