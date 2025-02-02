from fastapi import APIRouter
from app.controllers.auth_controller import AuthController

api_router = APIRouter()

auth_controller = AuthController()
api_router.include_router(auth_controller.router, prefix="/auth", tags=["Auth"])