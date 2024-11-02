import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from fastyr.api.main import app
from fastyr.core.contracts.request_dtos import AudioProcessRequest
from fastyr.core.exceptions import ValidationError
import base64

@pytest.mark.integration
class TestPipelineIntegration:
    @pytest.fixture(autouse=True)
    def setup(self, client: TestClient, mock_providers):
        self.client = client
        self.mock_stt, self.mock_llm, self.mock_tts = mock_providers
        
    @pytest.fixture
    def auth_headers(self):
        return {"Authorization": "Bearer test-token"}
        
    # def test_process_audio_success(self, client, auth_headers):
    #     # Arrange
    #     test_audio = base64.b64encode(b"test audio content").decode('utf-8')
    #     request = {
    #         "audio_data": test_audio,
    #         "request_id": "test-123",
    #         "user_id": "user-456"
    #     }
        
    #     # Act
    #     response = client.post(
    #         "/api/v1/pipeline/process",
    #         json=request,
    #         headers=auth_headers
    #     )
        
    #     # Assert
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["status"] == "completed"
    #     assert "audio_url" in data
        
    @pytest.mark.asyncio
    async def test_process_audio_validation_error(self, client):
        # Arrange
        invalid_request = {
            "audio_data": "",  # Empty audio data
            "request_id": "test-123"
        }
        
        # Act
        response = client.post(
            "/api/v1/pipeline/process",
            json=invalid_request,
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Assert
        assert response.status_code == 422