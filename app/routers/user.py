from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession 

from database import get_async_db_context
from models import UserModel, UserViewModel
from services import user as UserService
from services.exception import ResourceNotFoundError

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=list[UserViewModel])
async def get_all_users(async_db: AsyncSession = Depends(get_async_db_context)):
    return await UserService.get_users(async_db)

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserViewModel)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_async_db_context)):
    user = await UserService.get_user_by_id(db, user_id)
    
    if user is None:
        raise ResourceNotFoundError("User not found")
    return user 

@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserViewModel)
async def update_user(request: UserModel, user_id: int, db: AsyncSession = Depends(get_async_db_context)):
    user = await UserService.update_user(db, request, user_id)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_db_context)):
    await UserService.delete_user(db, user_id)
    return None