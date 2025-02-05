import enum
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, func, Enum
from sqlalchemy.orm import relationship
from app.database import Base

# ✅ Define Enum with lowercase values
class RoleEnum(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(Enum(RoleEnum, values_callable=lambda x: [e.value for e in x]), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="messages")
