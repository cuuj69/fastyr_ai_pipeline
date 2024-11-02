import pytest
from unittest.mock import AsyncMock, patch
from fastyr.services.providers.deepgram_provider import DeepgramProvider
from fastyr.services.providers.openai_provider import OpenAIProvider
from fastyr.services.providers.elevenlabs_provider import ElevenLabsProvider
from fastyr.core.exceptions import ProviderError

@pytest.mark.asyncio
class TestProviders:
    @pytest.fixture
    def mock_session(self):
        mock = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "results": {
                "channels": [{"alternatives": [{"transcript": "test text"}]}]
            }
        }
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_response
        mock.post.return_value = mock_context
        return mock

    async def test_deepgram_transcribe_success(self, mock_session):
        with patch('aiohttp.ClientSession', return_value=mock_session):
            provider = DeepgramProvider("test_key")
            provider.base_url = "https://api.deepgram.com/v1"
            result = await provider.transcribe(b"test audio")
            assert result == "test text"

    async def test_openai_generate_response_success(self, mock_session, monkeypatch):
        # Arrange
        provider = OpenAIProvider("test_key")
        provider.base_url = "https://api.openai.com/v1"  # Set base URL
        monkeypatch.setattr("aiohttp.ClientSession", lambda: mock_session)
        
        # Act
        result = await provider.generate_response("test prompt")
        
        # Assert
        assert result == "test response"

    async def test_openai_with_org_and_project(self, mock_session):
        # Arrange
        provider = OpenAIProvider(
            api_key="test_key",
            organization_id="org-test",
            project_id="proj-test"
        )
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "test response"}}]
        }
        mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        # Act
        result = await provider.generate_response(
            "test prompt",
            options={
                "temperature": 0.5,
                "max_tokens": 100,
                "stop": ["\n"]
            }
        )

        # Assert
        assert result == "test response"
        # Verify headers were set correctly
        mock_session.return_value.__aenter__.return_value.post.assert_called_once()
        call_kwargs = mock_session.return_value.__aenter__.return_value.post.call_args[1]
        assert call_kwargs["headers"]["OpenAI-Organization"] == "org-test"
        assert call_kwargs["headers"]["OpenAI-Project"] == "proj-test"