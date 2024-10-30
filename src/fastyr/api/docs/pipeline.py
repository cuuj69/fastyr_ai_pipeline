from fastapi.openapi.models import Example
from typing import Dict, Any

PIPELINE_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "process_audio": {
        "summary": "Process Audio Request",
        "description": "Example request for audio processing",
        "value": {
            "audio_data": "base64_encoded_audio_content",
            "request_id": "req-123",
            "user_id": "user-456",
            "options": {
                "language": "en",
                "quality": "high",
                "model": "gpt-4"
            }
        }
    },
    "process_response": {
        "summary": "Process Audio Response",
        "description": "Example response from audio processing",
        "value": {
            "id": 1,
            "status": "completed",
            "audio_url": "https://storage.example.com/processed/audio-123.wav",
            "created_at": "2024-01-01T12:00:00Z"
        }
    }
}

# Update the controller with enhanced documentation 