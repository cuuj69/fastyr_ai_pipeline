from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from jose import jwt
from fastyr.core.exceptions import AuthenticationError

security = HTTPBearer()

class SecurityMiddleware:
    def __init__(self, app):
        self.app = app
        
        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["X-Request-ID"]
        )
        
    async def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self.app.state.config.JWT_SECRET_KEY,
                algorithms=["HS256"]
            )
            return payload
        except Exception:
            raise AuthenticationError("Invalid token") 