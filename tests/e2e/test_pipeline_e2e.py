import pytest
import asyncio
from fastyr.domain.models.requests import AudioProcessRequest
from fastyr.services.providers.pipeline_service import PipelineService
from fastyr.infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository

@pytest.mark.e2e
async def test_complete_pipeline_flow(db_session):
    """Test complete pipeline flow with real services."""
    # Setup
    repo = SQLAlchemyRepository(db_session)
    service = PipelineService(
        repository=repo,
        stt_provider=RealSTTProvider(),
        llm_provider=RealLLMProvider(),
        tts_provider=RealTTSProvider()
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