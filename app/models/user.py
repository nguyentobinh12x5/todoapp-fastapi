from datetime import time
from pydantic import BaseModel

class CreateUserModel(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    is_admin: bool
    
    company_id: int
    
    class Config: 
        json_schema_extra = {
            "example": {
                "username": "admin",
                "email": "admin@gmail.com",
                "first_name": "admin",
                "last_name": "admin",
                "password": "admin",
                "is_admin": True,
                "company_id": 1
            }
        }
class UpdateUserModel(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    company_id: int
    
    class Config: 
        json_schema_extra = {
            "example": {
                "username": "admin",
                "email": "admin@gmail.com",
                "first_name": "admin",
                "last_name": "admin",
                "password": "admin",
                "company_id": 1
            }
        }

class UserModel(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    
    company_id: int

class UserBaseModel(BaseModel):
    id: int
    username: str
    email: str | None = None
    first_name: str
    last_name: str
    
    class Config:
        from_attributes = True

class UserViewModel(UserBaseModel):
    is_admin: bool
    company_id: int
    created_at: time | None = None
    updated_at: time | None = None

class UserClaims(BaseModel):
    sub: str
    username: str = None
    email: str = None
    email_verified: bool = False
    first_name: str
    last_name: str
    is_admin: bool = False
    aud: str = None
    iss: str = None
    iat: int
    exp: int