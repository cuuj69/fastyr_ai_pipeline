from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class AudioProcess(Base):
    __tablename__ = 'audio_processes'
    
    id = Column(Integer, primary_key=True)
    status = Column(String)
    audio_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow) 