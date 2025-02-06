from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage

class ChatMessageRepository:
    def get_all_chat_messages(self, db: Session, user_id: int):
        """Retrieve all chat messages for a user, ordered by creation time."""
        return (
            db.query(ChatMessage)
            .filter(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at)
            .all()
        )

    def add_message(self, db: Session, user_id: int, role: str, content: str):
        new_message = ChatMessage(user_id=user_id, role=role, content=content)
        db.add(new_message)
        return new_message


    def clear_chat(self, db: Session, user_id: str):
        """Delete all messages for a user safely."""
        db.query(ChatMessage).filter(ChatMessage.user_id == user_id).delete(synchronize_session='fetch')


    def get_latest_chat(self, db: Session, user_id: int, limit: int = 10):
        return (
            db.query(ChatMessage)
            .filter(ChatMessage.user_id == user_id)
            .order_by(desc(ChatMessage.created_at))  
            .limit(limit)
            .all()
        )