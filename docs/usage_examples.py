from fastyr.services.providers.pipeline_service import PipelineService
from fastyr.services.providers.deepgram_provider import DeepgramProvider
from fastyr.services.providers.openai_provider import OpenAIProvider
from fastyr.services.providers.elevenlabs_provider import ElevenLabsProvider
from fastyr.services.providers.local_storage_provider import LocalStorageProvider
from fastyr.core.contracts.request_dtos import AudioProcessRequest
from dotenv import load_dotenv
import asyncio
import os
from typing import Dict, Any
from fastyr.services.interfaces.llm_provider import LLMProvider

load_dotenv()

# Create a dummy LLM provider that just returns the input
class DummyLLMProvider(LLMProvider):
    async def generate_response(self, prompt: str, options: Dict[str, Any] = None) -> str:
        return prompt

async def basic_usage_example():
    """Basic usage example of the AI pipeline."""
    try:
        # Initialize providers
        storage = LocalStorageProvider(base_path="storage/audio")
        pipeline = PipelineService(
            stt_provider=DeepgramProvider(api_key=os.getenv('DEEPGRAM_API_KEY')),
            llm_provider=DummyLLMProvider(),  # Use dummy provider
            tts_provider=ElevenLabsProvider(
                api_key=os.getenv('ELEVENLABS_API_KEY'),
                voice_id="21m00Tcm4TlvDq8ikWAM"  # Default voice ID
            ),
            storage_provider=storage
        )

        # Process audio
        with open("/Users/admin/Documents/fastyr_ai_pipeline/test.wav", "rb") as f:
            audio_data = f.read()
        
        request = AudioProcessRequest(
            audio_data=audio_data,
            request_id="example-1",
            user_id="user-1",
            options={
                "language": "en",
                "quality": "high",
                # "llm_model": "gpt-3.5-turbo"
            }
        )
        
        result = await pipeline.process(request)
        print(f"Processed audio available at: {result.audio_url}")
        
    except Exception as e:
        print(f"Error processing audio: {str(e)}")

async def test_deepgram():
    stt_provider = DeepgramProvider(api_key=os.getenv('DEEPGRAM_API_KEY'))
    with open("/Users/admin/Documents/fastyr_ai_pipeline/docs/test_output.wav", "rb") as f:
        audio_data = f.read()
    transcript = await stt_provider.transcribe(audio_data)
    print(f"Transcription: {transcript}")

async def test_elevenlabs():
    tts_provider = ElevenLabsProvider(
        api_key=os.getenv('ELEVENLABS_API_KEY'),
        voice_id="21m00Tcm4TlvDq8ikWAM"
    )
    audio_data = await tts_provider.synthesize("This was built by William Jefferson Mensah")
    
    # Save the audio to test it
    with open("test_output.wav", "wb") as f:
        f.write(audio_data)
    print("Audio saved to test_output.wav")

if __name__ == "__main__":
    #asyncio.run(basic_usage_example())
    asyncio.run(test_deepgram())
    
    #asyncio.run(test_elevenlabs())