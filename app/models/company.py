from typing import Optional
from pydantic import BaseModel, Field
from entities.company import CompanyMode
from datetime import time

class SearchCompanyModel():
    def __init__(self, name, description, mode, rating, page, size) -> None:
        self.name = name
        self.description = description
        self.mode = mode
        self.rating = rating
        self.page = page
        self.size = size

class CompanyViewModel(BaseModel):
    id: int 
    name: str 
    description: Optional[str]
    mode: CompanyMode
    rating: float
    created_at: time
    updated_at: time
    
    class Config:
        from_attributes = True

class CreateCompanyModel(BaseModel):
    name: str
    description: Optional[str]
    mode: CompanyMode = Field(default=CompanyMode.PUBLIC)
    rating: float = Field(ge=0, le=5, default=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nashtech",
                "description": "Create the best solutions, powered by our excellence in people and technology",
                "mode": "public",
                "rating": "5"
            }
        }

class UpdateCompanyModel(BaseModel):
    name: str
    description: Optional[str]
    mode: CompanyMode = Field(default=CompanyMode.PUBLIC)
    rating: float = Field(None, ge=0, le=5)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nashtech",
                "description": "Create the best solutions, powered by our excellence in people and technology",
                "mode": "public",
                "rating": "5"
            }
        }