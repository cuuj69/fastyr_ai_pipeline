from abc import ABC, abstractmethod
from typing import List
from fastyr.core.contracts.response_dtos import AudioProcessResponse

class PipelineService(ABC):
    @abstractmethod
    async def process(self, audio_data: bytes, auth_data: dict) -> AudioProcessResponse:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int, auth_data: dict) -> AudioProcessResponse:
        pass
    
    @abstractmethod
    async def get_all(self, page: int, limit: int, auth_data: dict) -> List[AudioProcessResponse]:
        pass
