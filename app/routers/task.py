from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db_context
from models.task import CreateTaskModel, TaskViewModel, UpdateTaskModel
from services import task as TaskService
from services.exception import ResourceNotFoundError

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def get_task_by_id(
    task_id: int, 
    db: AsyncSession = Depends(get_async_db_context),
):
    task = await TaskService.get_task_by_id(db, task_id)
    
    if task is None:
        raise ResourceNotFoundError()
    
    return task

@router.get("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=list[TaskViewModel])
async def get_tasks_by_user_id(
    user_id: int, 
    db: AsyncSession = Depends(get_async_db_context),
):
    return await TaskService.get_tasks_by_user_id(db, user_id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel)
async def add_new_task(
    request: CreateTaskModel, 
    db: AsyncSession = Depends(get_async_db_context),
):
    return await TaskService.add_new_task(db, request)

@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def update_task(
    task_id: int, 
    request: UpdateTaskModel, 
    db: AsyncSession = Depends(get_async_db_context),
):
    task = await TaskService.update_task(db, task_id, request)
    
    if task is None:
        raise ResourceNotFoundError()
    
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int, 
    db: AsyncSession = Depends(get_async_db_context),
):
    await TaskService.delete_task(db, task_id)
    return None