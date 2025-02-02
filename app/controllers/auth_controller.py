from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService
from pydantic import BaseModel

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

    async def register(self, request: RegisterRequest, db: Session = Depends(get_db)):
        user = await self.auth_service.register_user(db, request.username, request.email, request.password)
        if not user:
            raise HTTPException(status_code=400, detail="Email already exists")
        return {"message": "User registered successfully"}

    async def login(self, request: LoginRequest, db: Session = Depends(get_db)):
        print('requestt', request)
        result = await self.auth_service.authenticate_user(db, request.email, request.password)
        if not result:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return result