from typing import TypeVar, Generic, Optional, List, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastyr.infrastructure.repositories.base import BaseRepository
from fastyr.domain.models.base import BaseModel

T = TypeVar('T', bound=BaseModel)

class SQLAlchemyRepository(BaseRepository[T]):
    """Generic SQLAlchemy repository implementation."""

    def __init__(self, session: AsyncSession, model_class: Type[T]):
        self.session = session
        self.model_class = model_class
    
    async def get_by_id(self, id:int) -> Optional[T]:
        query = select(self.model_class).where(self.model_class.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(self) -> List[T]:
        query = select(self.model_class)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def add(self, entity:T) -> T:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity
    
    async def update(self, entity: T) -> Optional[T]:
        await self.session.merge(entity)
        await self.session.flush()
        return entity
    
    async def delete(self, id: int) -> bool:
        entity = await self.get_by_id(id)
        if entity:
            await self.session.delete(entity)
            await self.session.flush()
            return True
        return False