from app.extensions import db
from sqlalchemy import func

class Profile(db.Model):
    __tablename__ = "profiles"

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id    = db.Column(db.Integer, unique=True, nullable=False)  # sem ForeignKey — isolamento de módulo
    
    # dados básicos
    nickname   = db.Column(db.String(64), nullable=False)
    handle     = db.Column(db.String(64), unique=True, nullable=False)
    bio        = db.Column(db.Text, nullable=True)
    avatar_id  = db.Column(db.String(32), nullable=True)  # file_id do storage

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Profile {self.nickname}>"


class Contact(db.Model):
    __tablename__ = "contacts"

    id                 = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_id         = db.Column(db.Integer, db.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    contact_profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    created_at         = db.Column(db.DateTime, server_default=func.now())

    # especifica qual FK cada relationship usa
    profile = db.relationship("Profile", foreign_keys=[profile_id],
                               backref=db.backref("contacts", lazy="dynamic", passive_deletes=True))
    
    contact_profile = db.relationship("Profile", foreign_keys=[contact_profile_id])

    __table_args__ = (
        db.UniqueConstraint("profile_id", "contact_profile_id", name="uq_contact"),
    )

    def __repr__(self):
        return f"<Contact {self.profile_id} → {self.contact_profile_id}>"