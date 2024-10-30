from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMProvider(ABC):
    """Interface for Language Model providers"""
    
    @abstractmethod
    async def generate_response(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """Generate response from prompt
        
        Args:
            prompt: Input text prompt
            options: Provider-specific options
            
        Returns:
            Generated response text
        """
        pass 