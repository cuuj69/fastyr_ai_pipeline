from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from fastyr.core.contracts.auth import AuthData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> AuthData:
    """Dependency to get the current authenticated user."""
    try:
        # TODO: Implement actual token validation
        # For now, return dummy auth data
        return AuthData(
            user_id="test-user",
            scopes=["pipeline:read", "pipeline:write"]
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) 