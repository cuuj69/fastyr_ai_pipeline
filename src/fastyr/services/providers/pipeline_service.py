from typing import Dict, Any
import asyncio
import random
import datetime
from fastyr.services.interfaces.stt_provider import STTProvider
from fastyr.services.interfaces.llm_provider import LLMProvider
from fastyr.services.interfaces.tts_provider import TTSProvider
from fastyr.core.exceptions import ProviderError
from fastyr.core.contracts.request_dtos import AudioProcessRequest
from fastyr.core.contracts.response_dtos import AudioProcessResponse

class PipelineService:
    def __init__(
        self,
        stt_provider: STTProvider,
        llm_provider: LLMProvider,
        tts_provider: TTSProvider,
        storage_provider: Any,
        max_retries: int = 3
    ):
        self.stt_provider = stt_provider
        self.llm_provider = llm_provider
        self.tts_provider = tts_provider
        self.storage_provider = storage_provider
        self.max_retries = max_retries
    
    async def _retry_with_backoff(self, operation, *args, **kwargs):
        """Execute operation with exponential backoff retry"""
        for attempt in range(self.max_retries):
            try:
                return await operation(*args, **kwargs)
            except ProviderError as e:
                if attempt == self.max_retries - 1:
                    raise
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                await asyncio.sleep(wait_time)
    
    async def process(self, request: AudioProcessRequest) -> AudioProcessResponse:
        """Process audio through the complete pipeline"""
        try:
            # 1. Speech to Text
            transcript = await self._retry_with_backoff(
                self.stt_provider.transcribe,
                request.audio_data,
                request.options.get("stt_options")
            )
            
            llm_response = transcript  # Just pass through the transcript for now
            
            # 3. Text to Speech
            audio_output = await self._retry_with_backoff(
                self.tts_provider.synthesize,
                llm_response,
                request.options.get("tts_options")
            )
            
            # Store the result
            audio_url = await self._store_audio(audio_output, request.request_id)
            
            return AudioProcessResponse(
                id=1,  # Use a numeric ID
                status="completed",
                audio_url=audio_url,
                request_id=request.request_id,
                created_at=datetime.datetime.utcnow()  # Use UTC timestamp
            )
            
        except ProviderError as e:
            raise ProviderError(
                f"Pipeline processing failed: {str(e)}"
            )
    
    async def _store_audio(self, audio_data: bytes, request_id: str) -> str:
        """Store audio data using the storage provider"""
        try:
            file_name = f"{request_id}.wav"
            return await self.storage_provider.store(audio_data, file_name)
        except Exception as e:
            raise ProviderError(f"Failed to store audio: {str(e)}")