import pytest
import asyncio
from fastyr.core.contracts.request_dtos import AudioProcessRequest
from fastyr.services.providers.pipeline_service import PipelineService
from fastyr.infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository

@pytest.mark.e2e
async def test_complete_pipeline_flow(db_session):
    """Test complete pipeline flow with real services."""
    from fastyr.domain.models.audio_process import AudioProcess
    
    # Setup
    repo = SQLAlchemyRepository(db_session, AudioProcess)
    service = PipelineService(
        repository=repo,
        stt_provider=AsyncMock(),  # Mock providers for e2e test
        llm_provider=AsyncMock(),
        tts_provider=AsyncMock(),
        storage_provider=AsyncMock()
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