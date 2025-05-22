from typing import Optional
from loguru import logger

from dto.profile import UserProfileDTO


class UserService:
    """Service for managing user data."""
    
    def __init__(self, firestore_service):
        """
        Initialize the user service.
        
        Args:
            firestore_service: Service for interacting with Firestore
        """
        self.firestore_service = firestore_service
        logger.info("User service initialized")
    
    def create_user(self, user_profile: UserProfileDTO) -> str:
        """
        Create a new user profile.
        
        Args:
            user_profile (UserProfileDTO): User profile data
            
        Returns:
            str: User ID
        """
        logger.info(f"Creating user profile for telegram_id: {user_profile.telegram_id}")
        return self.firestore_service.save_user(user_profile)
    
    def get_user(self, telegram_id: int) -> Optional[UserProfileDTO]:
        """
        Get a user profile by Telegram ID.
        
        Args:
            telegram_id (int): Telegram user ID
            
        Returns:
            Optional[UserProfileDTO]: User profile if found, None otherwise
        """
        logger.debug(f"Getting user profile for telegram_id: {telegram_id}")
        return self.firestore_service.get_user(telegram_id)
    
    def update_user(self, user_profile: UserProfileDTO) -> str:
        """
        Update a user profile.
        
        Args:
            user_profile (UserProfileDTO): User profile data
            
        Returns:
            str: User ID
        """
        logger.info(f"Updating user profile for telegram_id: {user_profile.telegram_id}")
        return self.firestore_service.save_user(user_profile)