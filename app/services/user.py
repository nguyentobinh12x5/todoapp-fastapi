from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import UserModel
from entities.user import User
from services.utils import get_current_utc_time
from services.exception import ResourceNotFoundError


async def get_users(async_db: AsyncSession) -> list[User]:
    result = await async_db.scalars(select(User).order_by(User.created_at))
    return result.all()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    result = await db.scalars(select(User).filter(User.id == user_id))
    return result.first()

async def update_user(db: AsyncSession, id: int, data: UserModel) -> User:
    user = await get_user_by_id(db, id)

    if user is None:
        raise ResourceNotFoundError()
    
    user.first_name = data.first_name
    user.last_name = data.last_name
    user.updated_at = get_current_utc_time()
    
    await db.commit()
    await db.refresh(user)

    return user


async def delete_user(db: AsyncSession, id: int) -> None:
    user = await get_user_by_id(db, id)

    if user is None:
        raise ResourceNotFoundError()
    
    await db.delete(user)
    await db.commit()