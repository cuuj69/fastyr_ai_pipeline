import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from fastyr.api.main import app
from fastyr.domain.models.requests import AudioProcessRequest
from fastyr.core.exceptions import ValidationError

@pytest.mark.integration
class TestPipelineIntegration:
    @pytest.fixture(autouse=True)
    def setup(self, client: TestClient):
        self.client = client
        
    async def test_process_audio_success(self):
        # Arrange
        test_file = b"test audio content"
        request = {
            "audio_data": test_file,
            "request_id": "test-123",
            "user_id": "user-456",
            "options": {
                "language": "en",
                "quality": "high"
            }
        }
        
        # Act
        response = await self.client.post(
            "/api/v1/pipeline/process",
            json=request,
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert "audio_url" in data
        
    async def test_process_audio_validation_error(self):
        # Arrange
        invalid_request = {
            "audio_data": "",  # Empty audio data
            "request_id": "test-123"
            # Missing user_id
        }
        
        # Act
        response = await self.client.post(
            "/api/v1/pipeline/process",
            json=invalid_request,
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Assert
        assert response.status_code == 400
        assert "validation error" in response.json()["message"].lower() 