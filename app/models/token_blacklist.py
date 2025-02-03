from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())