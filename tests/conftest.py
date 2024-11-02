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
async def db_session():
    """Create test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///./test.db")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close() 