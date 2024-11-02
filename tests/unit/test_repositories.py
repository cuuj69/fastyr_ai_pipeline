import pytest
from datetime import datetime
from fastyr.domain.models.audio_process import AudioProcess
from fastyr.infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository

@pytest.mark.asyncio
async def test_repository_crud_operations(db_session):
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