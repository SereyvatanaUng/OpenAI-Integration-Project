from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage

class ChatMessageRepository :
    # Get all chat messages for a user
    async def get_all_chat_messages(self, db: Session, user_id: int):
        return (
            db.query(ChatMessage)
            .filter(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at)
            .all()
        )

    # Add a new chat message (Setter)
    async def add_message(self, db: Session, user_id: int, role: str, content: str):
        new_message = ChatMessage(user_id=user_id, role=role, content=content)
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message

    # Clear all chat messages for a user
    async def clear_chat(self, db: Session, user_id: int):
        db.query(ChatMessage).filter(ChatMessage.user_id == user_id).delete()
        db.commit()