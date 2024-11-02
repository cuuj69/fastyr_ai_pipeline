import pytest
from datetime import datetime
from fastyr.core.contracts.request_dtos import AudioProcess
from fastyr.infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository

@pytest.mark.asyncio
async def test_repository_crud_operations(db_session):
    # Reference to existing test fixture
    """Reference to conftest.py"""
    startLine: 7
    endLine: 21
    
    # Arrange
    repo = SQLAlchemyRepository(db_session, AudioProcess)
    test_entity = AudioProcess(
        status="pending",
        audio_url="test.wav",
        created_at=datetime.utcnow()
    )
    
    # Act - Create
    created = await repo.add(test_entity)
    assert created.id is not None
    
    # Act - Read
    retrieved = await repo.get_by_id(created.id)
    assert retrieved.audio_url == test_entity.audio_url
    
    # Act - Update
    retrieved.status = "completed"
    updated = await repo.update(retrieved)
    assert updated.status == "completed"
    
    # Act - Delete
    deleted = await repo.delete(created.id)
    assert deleted is True 