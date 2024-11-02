from sqlalchemy import Column, Integer, String, DateTime
from fastyr.domain.models.base import Base

class AudioProcess(Base):
    __tablename__ = "audio_processes"
    
    id = Column(Integer, primary_key=True)
    status = Column(String)
    audio_url = Column(String)
    created_at = Column(DateTime)