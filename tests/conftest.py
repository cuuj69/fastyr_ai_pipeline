import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from fastyr.infrastructure.database.connection import async_session
from fastapi.testclient import TestClient
from fastyr.api.main import app
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def client():
    return TestClient(app)




@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine("sqlite+aiosqlite:///./test.db")
    async_session = sessionmaker(engine, class_=AsyncSession)
    async with async_session() as session:
        try:
            yield session
            await session.rollback()
        finally:
            await session.close() 