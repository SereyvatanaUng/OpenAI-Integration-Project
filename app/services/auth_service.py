from datetime import datetime, timedelta
from app.repositories.user_repository import UserRepository
from app.utils.security import hash_password, verify_password, create_access_token

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
            
        access_token = create_access_token({"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}