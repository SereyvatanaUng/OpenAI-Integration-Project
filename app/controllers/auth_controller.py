from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService
from app.utils.security import decode_access_token

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthController:
    def __init__(self):
        self.router = APIRouter()
        self.auth_service = AuthService()
        self.setup_routes()

    def setup_routes(self):
        self.router.post("/register")(self.register)
        self.router.post("/login")(self.login)
        self.router.post("/refresh-token")(self.refresh_token)
        self.router.post("/logout")(self.logout) 

    async def register(self, request: RegisterRequest, db: Session = Depends(get_db)):
        user = await self.auth_service.register_user(db, request.username, request.email, request.password)
        if not user:
            raise HTTPException(status_code=400, detail="Email already exists")
        return {"message": "User registered successfully"}

    async def login(self, request: LoginRequest, db: Session = Depends(get_db)):
        result = await self.auth_service.authenticate_user(db, request.email, request.password)
        if not result:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return result

    async def refresh_token(self, request: dict):
        refresh_token = request.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token is required")

        new_access_token = await self.auth_service.refresh_access_token(refresh_token)
        if not new_access_token:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        return new_access_token

    async def logout(self, authorization: str = Header(None), db: Session = Depends(get_db)):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=400, detail="Invalid token")

        token = authorization.split("Bearer ")[1]
        payload = decode_access_token(token)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"message": "Successfully logged out"}