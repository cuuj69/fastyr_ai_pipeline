import pytest
from fastapi.testclient import TestClient
from fastyr.api.main import app
from fastyr.core.di.container import Container
from fastyr.core.contracts.request_dtos import AudioProcessRequest
from fastyr.infrastructure.database.connection import get_db_url

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

@pytest.mark.asyncio
async def test_pipeline_integration(client):
    """Test complete pipeline flow."""
    # Arrange
    test_audio = b"test audio data"
    request = AudioProcessRequest(
        audio_data=test_audio,
        request_id="test-123",
        user_id="user-123"
    )
    
    # Act
    response = client.post(
        "/api/v1/pipeline/process",
        json=request.dict()
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "completed" 