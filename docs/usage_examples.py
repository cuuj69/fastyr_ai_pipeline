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


async def basic_usage_example():
    """Basic usage example of the AI pipeline."""
    try:
        # Initialize providers
        storage = LocalStorageProvider(base_path="storage/audio")
        pipeline = PipelineService(
            stt_provider=DeepgramProvider(api_key=os.getenv('DEEPGRAM_API_KEY')),
            llm_provider=OpenAIProvider(
                api_key=os.getenv('OPENAI_API_KEY'),
                model="gpt-4",  # or gpt-3.5-turbo 
                organization_id=os.getenv('OPENAI_ORG_ID')  # optional
            ),
            tts_provider=ElevenLabsProvider(
                api_key=os.getenv('ELEVENLABS_API_KEY'),
                voice_id="21m00Tcm4TlvDq8ikWAM" # this can be substituted for another voice from the voice library on elevenlabs.io
            ),
            storage_provider=storage
        )

        # Process audio
        with open("/Users/admin/Documents/fastyr_ai_pipeline/docs/test_output.wav", "rb") as f:
            audio_data = f.read()
        
        request = AudioProcessRequest(
            audio_data=audio_data,
            request_id="example-1",
            user_id="user-1",
            options={
                "llm_options": {
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "model": "gpt-4",
                    "top_p": 1.0,
                    "frequency_penalty": 0.0,
                    "presence_penalty": 0.0
                }
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
    audio_data = await tts_provider.synthesize("Who is sisyphus")
    
    # Save the audio to test it
    with open("test_output.wav", "wb") as f:
        f.write(audio_data)
    print("Audio saved to test_output.wav")

async def test_openai():
    llm_provider = OpenAIProvider(
        api_key=os.getenv('OPENAI_API_KEY'),
        model="gp-3.5-turbo",
        organization_id=os.getenv('OPENAI_API_ORGANIZATION_ID'),
        project_id=os.getenv('OPENAI_API_PROJECT_ID')
    )

    # Test with basic prompt
    prompt = "What is artificial intelligence in one sentence?"

    try:
        response = await llm_provider.generate_response(
            prompt,
            options={
                "temperature": 0.7,
                "max_tokens": 100,
                "model": "gpt-3.5-turbo",
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
        )
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error testing OpenAI: {str(e)}")

if __name__ == "__main__":
    asyncio.run(basic_usage_example())
    #asyncio.run(test_deepgram())
    #asyncio.run(test_elevenlabs())
    #asyncio.run(test_openai())