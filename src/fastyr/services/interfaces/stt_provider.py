from abc import ABC, abstractmethod
from typing import Dict, Any

class STTProvider(ABC):
    """Interface for Speech-to-Text providers"""
    
    @abstractmethod
    async def transcribe(self, audio_data: bytes, options: Dict[str, Any] = None) -> str:
        """Transcribe audio data to text
        
        Args:
            audio_data: Raw audio bytes
            options: Provider-specific options
            
        Returns:
            Transcribed text
        """
        pass 