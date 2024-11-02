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
        # Create mock response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "results": {
                "channels": [{"alternatives": [{"transcript": "test text"}]}]
            }
        }
        
        # Create session with proper async context manager
        session = AsyncMock()
        session.__aenter__.return_value = session
        
        # Create post response context
        post_cm = AsyncMock()
        post_cm.__aenter__.return_value = mock_response
        session.post.return_value = post_cm
        
        return session

    # async def test_deepgram_transcribe_success(self, mock_session):
    #     with patch('aiohttp.ClientSession', return_value=mock_session):
    #         provider = DeepgramProvider("test_key")
    #         result = await provider.transcribe(b"test audio")
    #         assert result == "test text"

    # async def test_openai_generate_response_success(self, mock_session):
    #     # Update mock response for OpenAI
    #     post_context = mock_session.post.return_value
    #     post_context.__aenter__.return_value.status = 200
    #     post_context.__aenter__.return_value.json.return_value = {
    #         "choices": [{"message": {"content": "test response"}}]
    #     }
        
    #     with patch('aiohttp.ClientSession', return_value=mock_session):
    #         provider = OpenAIProvider("test_key")
    #         result = await provider.generate_response("test prompt")
    #         assert result == "test response"

    # async def test_openai_with_org_and_project(self, mock_session):
    #     # Configure mock response
    #     post_cm = mock_session.post.return_value
    #     post_cm.__aenter__.return_value.status = 200
    #     post_cm.__aenter__.return_value.json.return_value = {
    #         "choices": [{"message": {"content": "test response"}}]
    #     }
        
    #     with patch('aiohttp.ClientSession', return_value=mock_session):
    #         provider = OpenAIProvider(
    #             api_key="test_key",
    #             organization_id="org-test",
    #             project_id="proj-test"
    #         )
    #         result = await provider.generate_response(
    #             "test prompt",
    #             options={
    #                 "temperature": 0.5,
    #                 "max_tokens": 100,
    #                 "stop": ["\n"]
    #             }
    #         )
    #         assert result == "test response"