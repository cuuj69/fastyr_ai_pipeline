from abc import ABC, abstractmethod
from typing import Dict, Any

class TTSProvider(ABC):
    """Interface for Text-to-Speech providers"""
    
    @abstractmethod
    async def synthesize(self, text: str, options: Dict[str, Any] = None) -> bytes:
        """Synthesize text to speech
        
        Args:
            text: Input text to synthesize
            options: Provider-specific options
            
        Returns:
            Raw audio bytes
        """
        pass 