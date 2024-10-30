import pytest
from unittest.mock import Mock, AsyncMock
from ...src.fastyr.services.providers.pipeline_service import PipelineService
from ...src.fastyr.core.exceptions import ValidationError
from ...src.fastyr.domain.models.requests import AudioProcessRequest

@pyttest.mark.asyncio
async def test_pipeline_service_validation():
    # Arrange
    mock_repo = AsyncMock()
    service = PipelineService(mock_repo)
    invalid_request = AudioProcessRequest(audio_data=b"", request_id="123", user_id="456")

    # Act & Assert
    with pytest.raises(ValidationError):
        await service.validate(invalid_request)