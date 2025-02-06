from sqlalchemy.orm import Session
from app.repositories.chat_message_repository import ChatMessageRepository

class ChatMessageService:
    def __init__(self, chat_repo: ChatMessageRepository):
        self.chat_repo = chat_repo

    def add_message(self, db: Session, user_id: str, role: str, content: str):
        """Add a new chat message and commit transaction."""
        message = self.chat_repo.add_message(db, user_id, role, content)
        db.commit()
        db.refresh(message)
        return message

    def clear_chat(self, db: Session, uesr_id: int):
        """Clear user chat messages and commit transaction."""
        self.chat_repo.clear_chat(db, uesr_id)
        db.commit()
