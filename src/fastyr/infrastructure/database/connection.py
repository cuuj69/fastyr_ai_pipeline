from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastyr.domain.models.base import Base
import os
from typing import AsyncGenerator
from fastapi import Depends

# Default to SQLite for testing if DATABASE_URL is not set
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./test.db"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Dependency for FastAPI
async def get_db_dependency():
    async with async_session() as session:
        yield session

def create_session_factory():
    return async_session

def get_db_url() -> str:
    """Get database URL from environment or return default test URL"""
    return os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./test.db"
    )
