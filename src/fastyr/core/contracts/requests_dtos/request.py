from pydantic import BaseModel

class AudioProcessRequest(BaseModel):
    file_url: str
    options: dict = {}

    class Config:
        schema_extra = {
            "example": {
                "file_url": "https://example.com/audio.mp3",
                "options": {
                    "language": "en-Us",
                    "model": "base"
                }
            }
        }