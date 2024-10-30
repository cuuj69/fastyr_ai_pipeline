from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Any

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """Base repository interface that defines common CRUD operations.
    
    This abstract class provides a contract for repository implementations
    to follow, ensuring consistent data access patterns across the application.
    
    Args:
        Generic[T]: The type of entity this repository handles
    """

    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[T]:
        """Retrieve and entity by its ID.
        
        Args:
            id: The unique identifier of the entity
        
        Returns:
            Optional[T]: The entity if found, None otherwise
        """
        pass
    @abstractmethod
    async def get_all(self) -> List[T]:
        """Retrieve all entities.
        
        Returns:
            List[T]: List of all entities
        """
        pass
    
    @abstractmethod
    async def add(self, entity: T) -> T:
        """Add a new entity.
        
        Args:
            entity: The entity to add
        
        Returns: 
            T: The added entity with any generated fields
        """
        pass
    
    @abstractmethod
    async def update(self,entity:T) -> Optional[T]:
        """Update an existing entity.
        
        Args:
            entity: The entity to update
            
        Returns:
            Optional[T]: The update entity if successful, None otherwise
        """
        pass

    @abstractmethod
    async def delete(self, id: Any) -> bool:
        """Delete an entity by its ID.
        
        Args:
            id: The unique identifier of the entity to delete
        
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        pass

        