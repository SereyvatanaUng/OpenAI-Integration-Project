from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException,Depends
from app.services.auth_service import AuthService
from sqlalchemy.orm import Session
from app.database import get_db

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.auth_service = AuthService()
        self.public_routes = ["/auth/login", "/auth/register"]  # Routes that do NOT require authentication


    async def dispatch(self, request, call_next,db: Session = Depends(get_db)):
        token = request.headers.get("Authorization")
        # Check if the request path is in public routes
        if request.url.path in self.public_routes:
            return await call_next(request)  # Skip authentication for public routes

        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized: No token provided")

        token = token.replace("Bearer ", "")
        # token = token.split("Bearer ")[1]

        
        # Validate the token
        user_data = await self.auth_service.validate_token(token,db)
        if not user_data:
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

        # Store user data in the request state so it can be used in the controller
        request.state.user = user_data

        response = await call_next(request)
        return response
