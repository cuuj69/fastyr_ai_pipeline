from fastyr.services.interfaces.stt_provider import STTProvider
from fastyr.core.exceptions import ProviderError
from fastyr.core.contracts.constants import ErrorCodes
from dotenv import load_dotenv
from typing import Dict, Any
import aiohttp
import os

load_dotenv()
DEEPGRAM_URL = os.getenv('DEEPGRAM_URL')
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

class DeepgramProvider(STTProvider):
    """Deepgram API provider implementation"""
    
    def __init__(self, api_key: str, base_url: str = DEEPGRAM_URL):
        self.api_key = api_key
        self.base_url = base_url
        
    async def transcribe(self, audio_data: bytes, options: Dict[str, Any] = None) -> str:
        """Transcribe audio using Deepgram API
        
        Args:
            audio_data: Raw audio bytes
            options: Additional options like model, language etc.
            
        Returns:
            Transcribed text
            
        Raises:
            ProviderError: If API call fails
        """
        async with aiohttp.ClientSession() as session:
            options = options or {}
            
            headers = {
                "Authorization": f"Token {self.api_key}",
                "Content-Type": "audio/wav"
            }
            
            params = {
                "model": options.get("model", "nova-2"),
                "language": options.get("language", "en")
            }
            
            try:
                async with session.post(
                    f"{self.base_url}/listen",
                    headers=headers,
                    data=audio_data,
                    params=params
                ) as response:
                    if response.status != 200:
                        error_data = await response.json()
                        raise ProviderError(
                            f"Deepgram API error: {error_data}",
                            code=ErrorCodes.PROVIDER_ERROR
                        )
                        
                    result = await response.json()
                    return result["results"]["channels"][0]["alternatives"][0]["transcript"]
                    
            except aiohttp.ClientError as e:
                raise ProviderError(
                    f"Failed to communicate with Deepgram API: {str(e)}",
                    code=ErrorCodes.PROVIDER_ERROR
                ) 