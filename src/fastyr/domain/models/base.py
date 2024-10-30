from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    """Base model with common fields for all entities."""
    __abstract__ = True

    id = Column(Integer, primary_key= True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate =datetime.utcnow)