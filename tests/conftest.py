import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastyr.infrastructure.database.connection import async_session

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.rollback()
        finally:
            await session.close() 