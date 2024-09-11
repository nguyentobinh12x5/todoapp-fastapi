from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import Base
from entities.base_entity import BaseEntity

class Task(BaseEntity, Base):
    __tablename__ = "tasks"

    summary = Column(String, nullable=False)   
    description = Column(String, nullable=True)
    status = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="tasks")
    
    
        