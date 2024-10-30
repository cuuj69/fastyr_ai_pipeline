import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastyr.infrastructure.database.connection import create_session_factory

@pytest.fixture
async def db_session() -> AsyncSession:
    session_factory = create_session_factory()
    async with session_factory() as session:
        yield session
        await session.rollback() 