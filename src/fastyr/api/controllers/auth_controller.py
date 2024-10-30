from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastyr.api.auth.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}