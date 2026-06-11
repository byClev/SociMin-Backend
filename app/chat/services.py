from app.extensions import db
from app.chat.models import Chat, Message
from app.chat.exceptions import (
    ChatNotFound,
    UnauthorizedAccess,
    ChatAlreadyExists,

)


class ChatService:

    # ── Chat ────────────────────────────────────

    def create_chat(self, user_id_1: int, user_id_2: int) -> Chat:

        existing = Chat.query.filter(
            ((Chat.user_id_1 == user_id_1) & (Chat.user_id_2 == user_id_2)) |
            ((Chat.user_id_1 == user_id_2) & (Chat.user_id_2 == user_id_1))
        ).first()

        if existing:
            raise ChatAlreadyExists()

        chat = Chat(user_id_1=user_id_1, user_id_2=user_id_2)
        db.session.add(chat)
        db.session.commit()
        return chat

    def get_chats(self, user_id: int, page: int = 1, per_page: int = 20):
        return (Chat.query
                .filter(
                    (Chat.user_id_1 == user_id) |
                    (Chat.user_id_2 == user_id)
                )
                .order_by(Chat.created_at.desc())
                .paginate(page=page, per_page=per_page, error_out=False))

    def _get_chat_or_raise(self, chat_id: int, user_id: int) -> Chat:
        conversation = Chat.query.get(chat_id)

        if not conversation:
            raise ChatNotFound()
        if user_id not in (conversation.user_id_1, conversation.user_id_2):
            raise UnauthorizedAccess()

        return conversation
    
    def delete_chat(self, chat_id: int, user_id: int) -> None:

        chat = self._get_chat_or_raise(chat_id, user_id)
        db.session.delete(chat)
        db.session.commit()

    # ── Message ─────────────────────────────────────────

    def send_message(self, chat_id: int, sender_id: int, content: str) -> Message:
        self._get_chat_or_raise(chat_id, sender_id)

        message = Message(
            chat_id         = chat_id,
            sender_id       = sender_id,
            content         = content
        )
        db.session.add(message)
        db.session.commit()
        return message

    def get_messages(self, chat_id: int, user_id: int,
                     after_id: int = None, page: int = 1, per_page: int = 20):
        self._get_chat_or_raise(chat_id, user_id)

        query = Message.query.filter_by(chat_id=chat_id)

        if after_id:
            query = query.filter(Message.id > after_id)

        return query.order_by(Message.created_at.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    def mark_as_read(self, chat_id: int, user_id: int) -> None:
        self._get_chat_or_raise(chat_id, user_id)

        (Message.query
         .filter_by(chat_id=chat_id, read=False)
         .filter(Message.sender_id != user_id)
         .update({"read": True}))

        db.session.commit()


chat_service = ChatService()