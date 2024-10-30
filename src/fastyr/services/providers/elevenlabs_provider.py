from typing import Dict, Any, List, Optional
import aiohttp
from fastyr.services.interfaces.tts_provider import TTSProvider
from fastyr.core.exceptions import ProviderError
from fastyr.core.contracts.constants import ErrorCodes
from dotenv import load_dotenv
import os

load_dotenv()
ELEVENLABS_URL = os.getenv('ELEVENLABS_URL')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

class PronunciationDictionary:
    def __init__(self, dictionary_id: str, version_id: str):
        self.dictionary_id = dictionary_id
        self.version_id = version_id

    def to_dict(self) -> Dict[str, str]:
        return {
            "pronunciation_dictionary_id": self.dictionary_id,
            "version_id": self.version_id
        }

class ElevenLabsProvider(TTSProvider):
    """ElevenLabs API provider implementation"""
    
    def __init__(self, 
                 api_key: str, 
                 voice_id: str = "default", 
                 base_url: str = ELEVENLABS_URL):
        self.api_key = api_key
        self.voice_id = voice_id
        self.base_url = base_url
    
    async def synthesize(self, text: str, options: Dict[str, Any] = None) -> bytes:
        """Synthesize text to speech using ElevenLabs API
        
        Args:
            text: Input text to synthesize
            options: Additional options including:
                - voice_id: Override default voice
                - model_id: Model to use (default: eleven_monolingual_v1)
                - language_code: Target language
                - stability: Voice stability (0-1)
                - similarity_boost: Voice similarity boost (0-1)
                - style: Style value (0-1)
                - use_speaker_boost: Enable speaker boost
                - pronunciation_dictionaries: List of PronunciationDictionary objects
                - seed: Random seed for synthesis
                - previous_text: Text that comes before
                - next_text: Text that comes after
                - previous_request_ids: List of previous request IDs
                - next_request_ids: List of next request IDs
                - use_pvc_as_ivc: Use PVC as IVC flag
                - apply_text_normalization: Text normalization mode
            
        Returns:
            Raw audio bytes
            
        Raises:
            ProviderError: If API call fails
        """
        options = options or {}
        voice_id = options.get("voice_id", self.voice_id)
        
        # Construct request payload
        payload = {
            "text": text,
            "model_id": options.get("model_id", "eleven_monolingual_v1"),
            "voice_settings": {
                "stability": options.get("stability", 0.5),
                "similarity_boost": options.get("similarity_boost", 0.8),
                "style": options.get("style", 0.0),
                "use_speaker_boost": options.get("use_speaker_boost", True)
            }
        }

        # Add optional parameters if provided
        if "language_code" in options:
            payload["language_code"] = options["language_code"]
            
        if "pronunciation_dictionaries" in options:
            payload["pronunciation_dictionary_locators"] = [
                d.to_dict() for d in options["pronunciation_dictionaries"]
            ]
            
        for field in ["seed", "previous_text", "next_text", "use_pvc_as_ivc"]:
            if field in options:
                payload[field] = options[field]
                
        if "previous_request_ids" in options:
            payload["previous_request_ids"] = options["previous_request_ids"]
            
        if "next_request_ids" in options:
            payload["next_request_ids"] = options["next_request_ids"]
            
        if "apply_text_normalization" in options:
            payload["apply_text_normalization"] = options["apply_text_normalization"]

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/text-to-speech/{voice_id}",
                    headers={
                        "xi-api-key": self.api_key,
                        "Content-Type": "application/json"
                    },
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_data = await response.json()
                        error_message = str(error_data) if error_data else f"Request failed with status {response.status}"
                        raise ProviderError(f"ElevenLabs API error: {error_message}")
                    
                    return await response.read()
                    
            except aiohttp.ClientError as e:
                raise ProviderError(
                    f"ElevenLabs API request failed: {str(e)}"
                )