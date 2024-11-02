import pytest
from unittest.mock import patch

@pytest.fixture
def mock_providers():
    with patch('fastyr.services.providers.deepgram_provider.DeepgramProvider') as mock_stt, \
         patch('fastyr.services.providers.openai_provider.OpenAIProvider') as mock_llm, \
         patch('fastyr.services.providers.elevenlabs_provider.ElevenLabsProvider') as mock_tts:
        
        mock_stt.return_value.transcribe.return_value = "test transcript"
        mock_llm.return_value.generate_response.return_value = "test response"
        mock_tts.return_value.synthesize.return_value = b"test audio"
        
        yield mock_stt, mock_llm, mock_tts 