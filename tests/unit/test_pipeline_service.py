import pytest
from unittest.mock import Mock, AsyncMock
from fastyr.services.providers.pipeline_service import PipelineService
from fastyr.core.exceptions import ValidationError
from fastyr.core.contracts.request_dtos import AudioProcessRequest

@pytest.mark.asyncio
async def test_pipeline_service_validation():
    # Arrange
    mock_storage = AsyncMock()
    mock_storage.store.return_value = "test_url.wav"
    
    service = PipelineService(
        stt_provider=AsyncMock(),
        llm_provider=AsyncMock(),
        tts_provider=AsyncMock(),
        storage_provider=mock_storage
    )
    
    request = AudioProcessRequest(
        audio_data=b"test audio",
        request_id="test-123",
        user_id="test-user"
    )
    
    result = await service.process(request)
    assert result.audio_url == "test_url.wav"