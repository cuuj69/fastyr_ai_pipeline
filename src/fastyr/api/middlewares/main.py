from fastapi import FastAPI
from fastapi.openai.utils import get_openapi
from fastyr.core.contracts.constants import API_VERSION

app = FastAPI(
    title="Fastyr AI Pipeline",
    description="Enterprise-grade AI pipeline for STT, LLM, and TTS processing",
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/doc"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Fastyr AI Pipeline",
        version=API_VERSION,
        description="Enterprise-grade AI pipeline for STT, LLM, and TTS processing",
        routes= app.routes
    )

    # Add Security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "auth/token",
                    "scopes": {
                        "pipeline:read": "Read pipeline data",
                        "pipeline:write": "Write pipeline data"
                    }
                }
            }
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
    