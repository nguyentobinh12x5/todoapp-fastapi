from sqlalchemy import Column, String, Enum, Float
from sqlalchemy.orm import relationship

from database import Base
from entities.base_entity import BaseEntity, CompanyMode

class Company(BaseEntity, Base):
    __tablename__ = "company"

    name = Column(String, nullable=False)   
    description = Column(String, nullable=True)
    mode = Column(Enum(CompanyMode), nullable=False, default=CompanyMode.PUBLIC)
    rating = Column(Float, nullable=False, default=0)   
    
    users = relationship("User", back_populates="company")