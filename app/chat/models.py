from app.extensions import db
from sqlalchemy import func

class Chat(db.Model):
    __tablename__ = "chats"

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id_1  = db.Column(db.Integer, nullable=False)
    user_id_2  = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    __table_args__ = (
        db.UniqueConstraint("user_id_1", "user_id_2", name="uq_chat_users"),
    )

    def __repr__(self):
        return f"<Chat {self.user_id_1} ↔ {self.user_id_2}>"


class Message(db.Model):
    __tablename__ = "messages"

    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id         = db.Column(db.Integer, db.ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    sender_id       = db.Column(db.Integer, nullable=False)
    content         = db.Column(db.Text, nullable=False)
    read            = db.Column(db.Boolean, default=False)
    created_at      = db.Column(db.DateTime, server_default=func.now())

    chat = db.relationship("Chat", backref=db.backref("messages", lazy="dynamic", passive_deletes=True))

    def __repr__(self):
        return f"<Message {self.id} from {self.sender_id}>"