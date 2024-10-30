from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from fastyr.core.contracts.auth import AuthData
from fastyr.services.providers.pipeline_service import PipelineService
from fastyr.api.dependencies.auth import get_current_user
from fastyr.core.contracts.request_dtos import AudioProcessRequest
from fastyr.core.contracts.response_dtos import AudioProcessResponse
from fastyr.core.exceptions import ValidationError
from fastyr.services.providers.deepgram_provider import DeepgramProvider
from fastyr.services.providers.openai_provider import OpenAIProvider
from fastyr.services.providers.elevenlabs_provider import ElevenLabsProvider
from fastyr.services.providers.local_storage_provider import LocalStorageProvider
import os

router = APIRouter(prefix="/api/v1/pipeline", tags=["pipeline"])

# Initialize providers and service
storage = LocalStorageProvider(base_path="storage")
pipeline_service = PipelineService(
    stt_provider=DeepgramProvider(api_key=os.getenv("DEEPGRAM_API_KEY")),
    llm_provider=OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY")),
    tts_provider=ElevenLabsProvider(api_key=os.getenv("ELEVENLABS_API_KEY")),
    storage_provider=storage
)

@router.post("/process")
async def process_audio(
    request: AudioProcessRequest = Body(...),
    auth: AuthData = Depends(get_current_user)
) -> AudioProcessResponse:
    try:
        result = await pipeline_service.process(request)
        return result
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
            
        