import pytest
from unittest.mock import Mock, AsyncMock
from fastyr.services.providers.pipeline_service import PipelineService
from fastyr.core.exceptions import ValidationError
from fastyr.core.contracts.request_dtos import AudioProcessRequest

@pytest.mark.asyncio
async def test_pipeline_service_validation():
    # Arrange
    mock_stt = AsyncMock()
    mock_llm = AsyncMock()
    mock_tts = AsyncMock()
    mock_storage = AsyncMock()
    
    service = PipelineService(
        stt_provider=mock_stt,
        llm_provider=mock_llm,
        tts_provider=mock_tts,
        storage_provider=mock_storage
    )
    
    # Create an invalid request
    request = AudioProcessRequest(
        audio_data=b"",  # Empty audio data
        request_id="test-123",
        user_id="test-user"
    )
    
    # Act & Assert
    with pytest.raises(ValidationError):
        await service.process(request)  # Use process instead of validate