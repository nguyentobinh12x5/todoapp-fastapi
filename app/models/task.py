from typing import Optional
from datetime import time, datetime
from pydantic import BaseModel

class TaskModel(BaseModel):
    id: int
    summary: str
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str] 
    
    user_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "summary": "Task 1",
                "description": "Task 1 description",
                "status": "In Progress",
                "priority": "1.0",
                "user_id": 1
            }
        }
class TaskViewModel(BaseModel):
    id: int
    summary: str
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str] 
    user_id: int
    created_at: time
    updated_at: time
    
    class Config:
        from_attributes = True

class CreateTaskModel(BaseModel):
    summary: str
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str] 
    
    user_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "Task 1",
                "description": "Task 1 description",
                "status": "In Progress",
                "priority": "1.0",
                "user_id": 1
            }
        }

class UpdateTaskModel(BaseModel):
    summary: str
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str] 
    
    user_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "Task 1",
                "description": "Task 1 description",
                "status": "In Progress",
                "priority": "1.0",
                "user_id": 1
            }
        }