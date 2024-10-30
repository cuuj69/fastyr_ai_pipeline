from abc import ABC, abstractmethod
from typing import BinaryIO, Optional

class StorageProvider(ABC):
    """Interface for storage providers"""
    
    @abstractmethod
    async def store(self, file_data: bytes, file_name: str) -> str:
        """Store file and return URL"""
        pass
    
    @abstractmethod
    async def retrieve(self, file_name: str) -> Optional[bytes]:
        """Retrieve file data by name"""
        pass
    
    @abstractmethod
    async def delete(self, file_name: str) -> bool:
        """Delete file by name"""
        pass 