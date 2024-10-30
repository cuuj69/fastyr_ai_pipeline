import pytest
from fastyr.services.providers.pipeline_service import PipelineService
from fastyr.services.providers.deepgram_provider import DeepgramProvider
from fastyr.services.providers.openai_provider import OpenAIProvider
from fastyr.services.providers.elevenlabs_provider import ElevenLabsProvider
from fastyr.services.providers.local_storage_provider import LocalStorageProvider
from fastyr.core.contracts.request_dtos import AudioProcessRequest

@pytest.mark.integration
class TestCompletePipeline:
    @pytest.fixture
    async def pipeline_service(self):
        # Use test API keys from environment variables
        storage = LocalStorageProvider(base_path="test_storage")
        service = PipelineService(
            stt_provider=DeepgramProvider(api_key="test_key"),
            llm_provider=OpenAIProvider(api_key="test_key"),
            tts_provider=ElevenLabsProvider(api_key="test_key"),
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