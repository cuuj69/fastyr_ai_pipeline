from pydantic import BaseModel
from typing import Dict, Any, Optional

class AudioProcessRequest(BaseModel):
    audio_data: bytes
    request_id: str
    user_id: str
    options: Dict[str, Any] = {} 