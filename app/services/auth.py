from typing import Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from entities.user import User
from models import CreateUserModel
from services.utils import get_current_utc_time, decode_token
from services.exception import InvalidInputError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def register_new_user(db: AsyncSession, data: CreateUserModel):
    existing_email_result = await db.scalars(select(User).filter(User.email == data.email))
    existing_email = existing_email_result.first()
    if existing_email:
        raise InvalidInputError("Email already exists")

    existing_username_result = await db.scalars(select(User).filter(User.username == data.username))
    existing_username = existing_username_result.first()
    if existing_username:
        raise InvalidInputError("Username already exists")
    
    hashed_password = get_password_hash(data.password)
    
    user = User(**data.model_dump())
    
    user.password = hashed_password
    user.created_at = get_current_utc_time()
    user.updated_at = get_current_utc_time()
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.scalars(select(User).filter(User.username == username))
    return result.first()
    
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_token(token)