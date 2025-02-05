from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.database import get_db

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.auth_service = AuthService()
        self.public_routes = ["/auth/login", "/auth/register"]  # Public routes

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            # Skip authentication for public routes
            if request.url.path in self.public_routes:
                return await call_next(request)

            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Unauthorized: No token provided")

            token = token.replace("Bearer ", "")

            # Use context manager to handle database session
            with next(get_db()) as db:
                user = await self.auth_service.validate_token(token, db)
                if not user:
                    raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

                request.state.user = user  # Store user info in request state

            return await call_next(request)
        
        except HTTPException as e:
            return Response(content=e.detail, status_code=e.status_code)
