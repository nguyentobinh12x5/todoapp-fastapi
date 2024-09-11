from sqlalchemy import Column, Time, Integer
from enum import Enum

class CompanyMode(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    NONPROFIT = "nonprofit"

class BaseEntity:
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(Time, nullable=False)
    updated_at = Column(Time, nullable=False)
