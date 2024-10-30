import os
import aiofiles
from pathlib import Path
from fastyr.services.interfaces.storage_provider import StorageProvider
from fastyr.core.exceptions import ProviderError
from typing import Optional

class LocalStorageProvider(StorageProvider):
    def __init__(self, base_path: str = "storage/audio"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    async def store(self, file_data: bytes, file_name: str) -> str:
        try:
            file_path = self.base_path / file_name
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(file_data)
            return str(file_path)
        except Exception as e:
            raise ProviderError(f"Failed to store file: {str(e)}")
    
    async def retrieve(self, file_name: str) -> Optional[bytes]:
        try:
            file_path = self.base_path / file_name
            if not file_path.exists():
                return None
            async with aiofiles.open(file_path, 'rb') as f:
                return await f.read()
        except Exception as e:
            raise ProviderError(f"Failed to retrieve file: {str(e)}")
    
    async def delete(self, file_name: str) -> bool:
        try:
            file_path = self.base_path / file_name
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            raise ProviderError(f"Failed to delete file: {str(e)}") 