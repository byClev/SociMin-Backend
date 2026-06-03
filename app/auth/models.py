from app.extensions import db
from datetime import datetime
from sqlalchemy import func

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'