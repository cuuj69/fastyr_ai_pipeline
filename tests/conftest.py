import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from fastyr.infrastructure.database.connection import async_session
from fastapi.testclient import TestClient
from fastyr.api.main import app
from sqlalchemy.orm import sessionmaker
from fastyr.infrastructure.database.connection import Base
from fastyr.domain.models.audio_process import AudioProcess
from unittest.mock import patch, AsyncMock
import base64



@pytest.fixture
def client():
    return TestClient(app)




@pytest.fixture
async def db_session():
    """Create test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            # Clean up
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all) 



@pytest.fixture
def mock_providers():
    storage_mock = AsyncMock()
    storage_mock.store.return_value = "test_url.wav"
    
    stt_mock = AsyncMock()
    stt_mock.transcribe.return_value = "test transcript"
    
    llm_mock = AsyncMock()
    llm_mock.generate_response.return_value = "test response"
    
    tts_mock = AsyncMock()
    tts_mock.synthesize.return_value = b"test audio"
    
    # Patch at the dependency injection level
    with patch('fastyr.core.di.container.LocalStorageProvider', return_value=storage_mock), \
         patch('fastyr.core.di.container.DeepgramProvider', return_value=stt_mock), \
         patch('fastyr.core.di.container.OpenAIProvider', return_value=llm_mock), \
         patch('fastyr.core.di.container.ElevenLabsProvider', return_value=tts_mock):
        yield storage_mock, stt_mock, llm_mock, tts_mock 