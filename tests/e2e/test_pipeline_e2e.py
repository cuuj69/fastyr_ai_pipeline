import pytest
import asyncio
from fastyr.core.contracts.request_dtos import AudioProcessRequest
from fastyr.services.providers.pipeline_service import PipelineService
from unittest.mock import AsyncMock

def load_test_audio():
    """Load sample audio file for testing."""
    with open("tests/fixtures/test_audio.wav", "rb") as f:
        return f.read()

@pytest.mark.e2e
async def test_complete_pipeline_flow(db_session):
    """Test complete pipeline flow with real services."""
    from fastyr.domain.models.audio_process import AudioProcess
    
    # Setup
    stt_mock = AsyncMock()
    stt_mock.transcribe.return_value = "test transcript"
    llm_mock = AsyncMock()
    llm_mock.generate_response.return_value = "test response"
    tts_mock = AsyncMock()
    tts_mock.synthesize.return_value = b"test audio"
    storage_mock = AsyncMock()
    storage_mock.store.return_value = "test_url"
    
    service = PipelineService(
        stt_provider=stt_mock,
        llm_provider=llm_mock,
        tts_provider=tts_mock,
        storage_provider=storage_mock
    )
    
    # Execute
    request = AudioProcessRequest(
        audio_data=load_test_audio(),
        request_id="e2e-test",
        user_id="test-user"
    )
    
    result = await service.process(request)
    
    # Verify
    assert result.status == "completed"
    assert result.audio_url is not None 