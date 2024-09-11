# Stable Import
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import timedelta


from database import get_async_db_context

from models import CreateUserModel, UserViewModel
from services import auth as AuthService
from services.exception import UnAuthorizedError
from services.utils import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
async def login_for_access_token(data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_db_context)):
    user = await AuthService.authenticate_user(db, data.username, data.password)
    if not user:
        raise UnAuthorizedError()
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(user, expires=int(access_token_expires.total_seconds()))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserViewModel)
async def register_new_user(request: CreateUserModel, db: AsyncSession = Depends(get_async_db_context)):
    user = await AuthService.register_new_user(db, request)
    return user
