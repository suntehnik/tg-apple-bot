from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractScenario(ABC):
    """Base abstract class for all scenarios."""
    
    @abstractmethod
    async def start(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start the scenario.
        
        Args:
            context (Dict[str, Any]): Context information including user_id, chat_id, etc.
            
        Returns:
            Dict[str, Any]: Updated context with scenario state
        """
        pass
    
    @abstractmethod
    async def next_step(self, context: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the next step in the scenario.
        
        Args:
            context (Dict[str, Any]): Current scenario context
            input_data (Dict[str, Any]): Input data from the user
            
        Returns:
            Dict[str, Any]: Updated context with scenario state
        """
        pass
    
    @abstractmethod
    async def cancel(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cancel the scenario.
        
        Args:
            context (Dict[str, Any]): Current scenario context
            
        Returns:
            Dict[str, Any]: Final context after cancellation
        """
        pass