from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from entities.base_entity import BaseEntity

from entities.task import Task
from entities.company import Company

class User(BaseEntity, Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    company_id = Column(Integer, ForeignKey('company.id'))

    tasks = relationship("Task", back_populates="user")
    company = relationship("Company", back_populates="users")
