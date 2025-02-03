from sqlalchemy.orm import Session
from app.models.token_blacklist import TokenBlacklist

class TokenRepository:
    def add_blacklisted_token(self, db: Session, token: str):
        blacklisted_token = TokenBlacklist(token=token)
        db.add(blacklisted_token)
        db.commit()

    def is_token_blacklisted(self, db: Session, token: str) -> bool:
        return db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first() is not None
