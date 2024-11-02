import pytest
from fastapi.testclient import TestClient
from fastyr.api.main import app
from fastyr.core.di.container import Container
from fastyr.core.contracts.request_dtos import AudioProcessRequest
from fastyr.infrastructure.database.connection import get_db_url
import base64
from unittest.mock import patch, AsyncMock

@pytest.fixture
def client():
    """Create test client with test container."""
    container = Container()
    container.config.from_dict({
        "db": {"url": get_db_url()},
        "sentry": {"dsn": ""},
    })
    app.container = container
    return TestClient(app)

@pytest.fixture
def mock_providers():
    with patch('fastyr.services.providers.deepgram_provider.DeepgramProvider') as mock_stt, \
         patch('fastyr.services.providers.openai_provider.OpenAIProvider') as mock_llm, \
         patch('fastyr.services.providers.elevenlabs_provider.ElevenLabsProvider') as mock_tts:
        
        mock_stt.return_value.transcribe.return_value = "test transcript"
        mock_llm.return_value.generate_response.return_value = "test response"
        mock_tts.return_value.synthesize.return_value = b"test audio"
        
        yield mock_stt, mock_llm, mock_tts

# @pytest.mark.asyncio
# async def test_pipeline_integration(client, mock_providers):
#     """Test complete pipeline flow."""
#     # Arrange
#     mock_stt, mock_llm, mock_tts = mock_providers
    
#     # Configure mock responses
#     mock_stt.transcribe.return_value = "test transcript"
#     mock_llm.generate_response.return_value = "test response"
#     mock_tts.synthesize.return_value = b"test audio"
    
#     # Test setup and execution
#     audio_data = base64.b64encode(b"test audio data").decode('utf-8')
#     request = {
#         "audio_data": audio_data,
#         "request_id": "test-123",
#         "user_id": "user-123"
#     }
#     headers = {"Authorization": "Bearer test-token"}
    
#     response = client.post(
#         "/api/v1/pipeline/process",
#         json=request,
#         headers=headers
#     )
    
#     # Assert
#     assert response.status_code == 200
#     data = response.json()
#     assert data["status"] == "completed"
#     assert "audio_url" in data