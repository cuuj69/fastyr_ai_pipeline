import pytest
from fastyr.services.providers.pipeline_service import PipelineService
from fastyr.services.providers.deepgram_provider import DeepgramProvider
from fastyr.services.providers.openai_provider import OpenAIProvider
from fastyr.services.providers.elevenlabs_provider import ElevenLabsProvider
from fastyr.services.providers.local_storage_provider import LocalStorageProvider
from fastyr.core.contracts.request_dtos import AudioProcessRequest
from unittest.mock import AsyncMock

@pytest.mark.integration
class TestCompletePipeline:
    @pytest.fixture
    async def pipeline_service(self):
        storage = AsyncMock()
        storage.store.return_value = "test_url.wav"
        
        stt_mock = AsyncMock()
        stt_mock.transcribe.return_value = "test transcript"
        
        llm_mock = AsyncMock()
        llm_mock.generate_response.return_value = "test response"
        
        tts_mock = AsyncMock()
        tts_mock.synthesize.return_value = b"test audio"
        
        service = PipelineService(
            stt_provider=stt_mock,
            llm_provider=llm_mock,
            tts_provider=tts_mock,
            storage_provider=storage
        )
        return service

    async def test_complete_pipeline_flow(self, pipeline_service):
        # Arrange
        request = AudioProcessRequest(
            audio_data=b"test audio content",
            request_id="test-123",
            user_id="test-user",
            options={
                "language": "en",
                "quality": "high"
            }
        )

        # Act
        result = await pipeline_service.process(request)

        # Assert
        assert result.status == "completed"
        assert result.audio_url is not None 