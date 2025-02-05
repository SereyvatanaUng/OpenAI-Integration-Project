from app.repositories.user_repository import UserRepository
from app.utils.security import (
    decode_access_token, hash_password, verify_password,
    create_access_token, create_refresh_token, decode_refresh_token
)
from sqlalchemy.orm import Session

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def register_user(self, db, username: str, email: str, password: str):
        if await self.user_repository.get_user_by_email(db, email):
            return None
            
        user_data = {
            "username": username,
            "email": email,
            "password_hash": hash_password(password)
        }
        return await self.user_repository.create_user(db, user_data)

    async def authenticate_user(self, db, email: str, password: str):
        user = await self.user_repository.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            return None
            
        access_token = create_access_token({"id": user.id, "email": user.email})
        refresh_token = create_refresh_token({"id": user.id, "email": user.email})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def refresh_access_token(self, refresh_token: str):
        payload = decode_refresh_token(refresh_token)
        if not payload:
            return None

        new_access_token = create_access_token({"id": payload["id"], "email": payload["email"]})

        return {"access_token": new_access_token, "token_type": "bearer"}

    async def validate_token(self, token: str, db: Session):
        payload = decode_access_token(token)
        if not payload:
            return None

        user_id = payload.get("id")
        email = payload.get("email")

        if not user_id or not email:
            return None
        
        return {"id": user_id, "email": email}
