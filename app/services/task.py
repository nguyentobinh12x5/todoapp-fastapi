from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from entities.task import Task
from models.task import CreateTaskModel, UpdateTaskModel
from services import user as UserService
from services.utils import get_current_utc_time
from services.exception import ResourceNotFoundError, InvalidInputError

async def get_task_by_id(db: AsyncSession, id: int, /, joined_load=False) -> Task:
    query = select(Task).filter(Task.id == id)
    
    if joined_load:
        query = query.options(joinedload(Task.user, innerjoin=True))
    
    result = await db.scalars(query)
    return result.first()

async def get_tasks_by_user_id(db: AsyncSession, user_id: int, /) -> list[Task]:
    query = select(Task).filter(Task.user_id == user_id)
    result = await db.scalars(query)
    return result.all()

async def add_new_task(db: AsyncSession, data: CreateTaskModel) -> Task:
    user = await UserService.get_user_by_id(db, data.user_id)
        
    if user is None:
        raise InvalidInputError("Invalid author information")

    task = Task(**data.model_dump())
    
    task.created_at = get_current_utc_time()
    task.updated_at = get_current_utc_time()

    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    return task

async def update_task(db: AsyncSession, id: int, data: UpdateTaskModel) -> Task:
    task = await get_task_by_id(db, id)

    if task is None:
        raise ResourceNotFoundError()

    if data.user_id != task.user_id:
        user = await UserService.get_user_by_id(db, data.user_id)
        if user is None:
            raise InvalidInputError("Invalid author information")
    
    task.summary = data.summary
    task.description = data.description
    task.status = data.status
    task.priority = data.priority
    task.updated_at = get_current_utc_time()
    
    await db.commit()
    await db.refresh(task)
    
    return task

async def delete_task(db: AsyncSession, id: int) -> None:
    task = await get_task_by_id(db, id)
    
    if task is None:
        raise ResourceNotFoundError()
    
    await db.delete(task)
    await db.commit()
    
    return None