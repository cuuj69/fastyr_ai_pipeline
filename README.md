
# Fastyr AI Pipeline

A flexible and extensible Python library for building AI-powered conversational pipelines. Fastyr provides a clean interface between Speech-to-Text (STT), Language Model (LLM), and Text-to-Speech (TTS) services.

## Features

- 🔄 Seamless integration of STT, LLM, and TTS services
- 🔌 Easy provider switching with consistent interfaces
- 🚀 Async/await support for optimal performance
- 🛡️ Built-in error handling and retries
- 📦 No dependency on provider-specific client libraries
- 💾 Flexible storage backend support
- ✅ Comprehensive test coverage

## Installation

pip install fastyr-ai-pipeline

## Quick Start


from fastyr.services.providers.pipeline_service import PipelineService
from fastyr.services.providers.deepgram_provider import DeepgramProvider
from fastyr.services.providers.openai_provider import OpenAIProvider
from fastyr.services.providers.elevenlabs_provider import ElevenLabsProvider
from fastyr.services.providers.local_storage_provider import LocalStorageProvider

Initialize providers

storage = LocalStorageProvider(base_path="storage/audio")
pipeline = PipelineService(
stt_provider=DeepgramProvider(api_key=os.getenv('DEEPGRAM_API_KEY')),
llm_provider=OpenAIProvider(api_key=os.getenv('OPENAI_API_KEY')),
tts_provider=ElevenLabsProvider(
api_key=os.getenv('ELEVENLABS_API_KEY'),
voice_id="your-voice-id"
),
storage_provider=storage
)
result = await pipeline.process(request)
print(f"Processed audio available at: {result.audio_url}")


## Architecture

### Provider Interfaces

The library defines three core interfaces:

1. **STTProvider**: Speech-to-Text interface
   - `transcribe(audio_data: bytes, options: Dict) -> str`

2. **LLMProvider**: Language Model interface
   - `generate_response(prompt: str, options: Dict) -> str`

3. **TTSProvider**: Text-to-Speech interface
   - `synthesize(text: str, options: Dict) -> bytes`

### Implemented Providers

1. **Deepgram** (STT)
   - High-accuracy speech recognition
   - Supports multiple languages
   - Configurable models

2. **OpenAI** (LLM)
   - GPT-3.5/4 integration
   - Customizable prompts
   - Temperature and other parameter controls

3. **ElevenLabs** (TTS)
   - High-quality voice synthesis
   - Multiple voice options
   - Adjustable speech parameters

## Configuration

Create a `.env` file in your project root:

DEEPGRAM_API_KEY=your_deepgram_key
DEEPGRAM_URL=https://api.deepgram.com/v1
OPENAI_API_KEY=your_openai_key
OPENAI_URL=https://api.openai.com/v1
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_URL=https://api.elevenlabs.io/v1



## Advanced Usage

### Custom Provider Implementation

Create your own provider by implementing the relevant interface:
from fastyr.services.interfaces.stt_provider import STTProvider
class CustomSTTProvider(STTProvider):
async def transcribe(self, audio_data: bytes, options: Dict[str, Any] = None) -> str:
# `from fastyr.services.interfaces.stt_provider import STTProvider
class CustomSTTProvider(STTProvider):
async def transcribe(self, audio_data: bytes, options: Dict[str, Any] = None) -> str: 
pass
`
### Error Handling

The library provides built-in error handling:
python
try:
result = await pipeline.process(request)
except ProviderError as e:
print(f"Provider error: {e}")
except ValidationError as e:
print(f"Validation error: {e}")


### FastAPI Integration
python
from fastapi import FastAPI, Depends
from fastyr.api.controllers.pipeline_controller import router as pipeline_router
app = FastAPI()
app.include_router(pipeline_router)


## Testing

Run the test suite:

Run specific test categories:
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/


## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Author

William Jefferson Mensah
- Email: mensahjefferson69@gmail.com
- GitHub: [@cuuj69](https://github.com/cuuj69)

## Requirements

- Python ≥ 3.7
- FastAPI ≥ 0.68.0
- SQLAlchemy ≥ 1.4.0
- Other dependencies listed in setup.py

## Support

For support, please open an issue on the GitHub repository or contact the author directly.


To run the project:
# From the project root
uvicorn src.fastyr.api.main:app --reload 

