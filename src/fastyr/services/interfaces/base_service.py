from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from fastyr.core.contracts.auth import AuthData

InputT = TypeVar('InputT')
OutputT = TypeVar('Output')

class BaseService(ABC, Generic[InputT, OutputT]):
    """Base interface for all services"""

    @abstractmethod
    async def process(
        self,
        input_data: InputT,
        auth: Optional[AuthData] = None
    ) -> OutputT:
        """Process the input data and return output 
        
        Args:
            input_data: The input data to process
            auth: Optional authentication data
        
        Returns:
            The processed output
        
        Raises:
            ServiceError: If processing fails
        """
        pass
    
    @abstractmethod
    async def validate(self, input_data: InputT) -> bool:
        """Validate the input data.
        
        Args:
            input_data: The input data to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        pass