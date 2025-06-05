from typing import List, Optional, Dict, Any
from datetime import datetime
from loguru import logger

from dto.meal import MealDTO


class MealService:
    """Service for managing meal data."""
    
    def __init__(self, firestore_service):
        """
        Initialize the meal service.
        
        Args:
            firestore_service: Service for interacting with Firestore
        """
        self.firestore_service = firestore_service
        logger.info("Meal service initialized")
    
    def add_meal(self, user_id: str, meal: MealDTO) -> str:
        """
        Add a new meal record.
        
        Args:
            user_id (str): User ID
            meal (MealDTO): Meal data
            
        Returns:
            str: Meal ID
        """
        logger.info(f"Adding meal record for user_id: {user_id}")
        
        # Ensure user ID is set
        meal.user_id = user_id
        
        return self.firestore_service.save_meal(meal)
    
    def get_user_meals(self, user_id: str, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None) -> List[MealDTO]:
        """
        Get meal records for a user.
        
        Args:
            user_id (str): User ID
            from_date (Optional[datetime]): Start date for filtering
            to_date (Optional[datetime]): End date for filtering
            
        Returns:
            List[MealDTO]: List of meal records
        """
        logger.debug(f"Getting meal records for user_id: {user_id}")
        return self.firestore_service.get_meals(user_id, from_date, to_date)
    
    def get_user_stats(self, user_id: str, days: int = 7) -> Dict[str, Any]:
        """
        Get nutrition statistics for a user.
        
        Args:
            user_id (str): User ID
            days (int): Number of days to include in statistics
            
        Returns:
            Dict[str, Any]: Statistics including total and average values
        """
        logger.info(f"Generating statistics for user_id: {user_id}")
        return self.firestore_service.get_user_stats(user_id, days)