import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
from loguru import logger

from config.config import Config
from dto.profile import UserProfileDTO
from dto.meal import MealDTO


class FirestoreService:
    """Service for interacting with Google Firestore."""
    
    def __init__(self, config: Config):
        """
        Initialize the Firestore service.
        
        Args:
            config (Config): Application configuration
        """
        self.config = config
        
        # Check if credentials file exists
        if not os.path.exists(config.firestore_credentials_path):
            raise FileNotFoundError(f"Firestore credentials file not found: {config.firestore_credentials_path}")
        
        # Initialize Firebase app
        try:
            cred = credentials.Certificate(config.firestore_credentials_path)
            self.app = firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            logger.info("Firestore service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Firestore: {str(e)}")
            raise
    
    def save_user(self, user_profile: UserProfileDTO) -> str:
        """
        Save a user profile to Firestore.
        
        Args:
            user_profile (UserProfileDTO): User profile data
            
        Returns:
            str: Document ID of the saved profile
        """
        try:
            users_ref = self.db.collection('users')
            
            # Check if user already exists
            query = users_ref.where('telegram_id', '==', user_profile.telegram_id).limit(1)
            existing_users = list(query.stream())
            
            if existing_users:
                # Update existing user
                user_ref = existing_users[0].reference
                user_ref.update(user_profile.to_dict())
                logger.info(f"Updated user profile for telegram_id: {user_profile.telegram_id}")
                return existing_users[0].id
            else:
                # Create new user
                doc_ref = users_ref.add(user_profile.to_dict())
                logger.info(f"Created new user profile for telegram_id: {user_profile.telegram_id}")
                return doc_ref[1].id
                
        except Exception as e:
            logger.error(f"Error saving user profile: {str(e)}")
            raise
    
    def get_user(self, telegram_id: int) -> Optional[UserProfileDTO]:
        """
        Get a user profile by Telegram ID.
        
        Args:
            telegram_id (int): Telegram user ID
            
        Returns:
            Optional[UserProfileDTO]: User profile if found, None otherwise
        """
        try:
            users_ref = self.db.collection('users')
            query = users_ref.where('telegram_id', '==', telegram_id).limit(1)
            users = list(query.stream())
            
            if users:
                user_data = users[0].to_dict()
                return UserProfileDTO.from_dict(users[0].id, user_data)
            else:
                logger.warning(f"User not found with telegram_id: {telegram_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting user profile: {str(e)}")
            raise
    
    def save_meal(self, meal: MealDTO) -> str:
        """
        Save a meal record to Firestore.
        
        Args:
            meal (MealDTO): Meal data
            
        Returns:
            str: Document ID of the saved meal
        """
        try:
            meals_ref = self.db.collection('meals')
            doc_ref = meals_ref.add(meal.to_dict())
            logger.info(f"Saved meal record for user_id: {meal.user_id}")
            return doc_ref[1].id
                
        except Exception as e:
            logger.error(f"Error saving meal record: {str(e)}")
            raise
    
    def get_meals(self, user_id: str, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None) -> List[MealDTO]:
        """
        Get meal records for a user.
        
        Args:
            user_id (str): User ID
            from_date (Optional[datetime]): Start date for filtering
            to_date (Optional[datetime]): End date for filtering
            
        Returns:
            List[MealDTO]: List of meal records
        """
        try:
            meals_ref = self.db.collection('meals')
            query = meals_ref.where('user_id', '==', user_id)
            
            # Apply date filters if provided
            if from_date:
                query = query.where('timestamp', '>=', from_date)
            
            if to_date:
                query = query.where('timestamp', '<=', to_date)
            
            # Sort by timestamp in descending order
            query = query.order_by('timestamp', direction=firestore.Query.DESCENDING)
            
            # Get results
            meals = []
            for doc in query.stream():
                meal_data = doc.to_dict()
                meals.append(MealDTO.from_dict(doc.id, meal_data))
            
            logger.info(f"Retrieved {len(meals)} meal records for user_id: {user_id}")
            return meals
                
        except Exception as e:
            logger.error(f"Error getting meal records: {str(e)}")
            raise
    
    def get_user_stats(self, user_id: str, days: int = 7) -> Dict[str, Any]:
        """
        Get nutrition statistics for a user.
        
        Args:
            user_id (str): User ID
            days (int): Number of days to include in statistics
            
        Returns:
            Dict[str, Any]: Statistics including total and average values
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get meals for the period
            meals = self.get_meals(user_id, from_date=start_date, to_date=end_date)
            
            # Initialize statistics
            stats = {
                "total": {
                    "calories": 0,
                    "proteins": 0,
                    "fats": 0,
                    "carbs": 0
                },
                "average": {
                    "calories": 0,
                    "proteins": 0,
                    "fats": 0,
                    "carbs": 0
                },
                "meals_count": len(meals),
                "days": days
            }
            
            # Calculate totals
            for meal in meals:
                stats["total"]["calories"] += meal.calories
                stats["total"]["proteins"] += meal.proteins
                stats["total"]["fats"] += meal.fats
                stats["total"]["carbs"] += meal.carbs
            
            # Calculate averages
            if days > 0:
                stats["average"]["calories"] = stats["total"]["calories"] / days
                stats["average"]["proteins"] = stats["total"]["proteins"] / days
                stats["average"]["fats"] = stats["total"]["fats"] / days
                stats["average"]["carbs"] = stats["total"]["carbs"] / days
            
            logger.info(f"Generated statistics for user_id: {user_id} over {days} days")
            return stats
                
        except Exception as e:
            logger.error(f"Error generating user statistics: {str(e)}")
            raise