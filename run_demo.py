#!/usr/bin/env python3
"""
Demo script to test the bot without dependencies
This allows testing the structure without installing all dependencies
"""

import os
import sys
import json
import logging
from datetime import datetime

# Configure basic logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("food-bot-demo")

# Simplified Config class
class Config:
    def __init__(self, **kwargs):
        self.telegram_token = kwargs.get("telegram_token", "demo_token")
        self.openai_api_key = kwargs.get("openai_api_key", "demo_key")
        self.firestore_credentials_path = kwargs.get("firestore_credentials_path", "secrets/firebase-credentials.json")
        self.log_level = kwargs.get("log_level", "DEBUG")

# Simplified ConfigManager class
class ConfigManager:
    def __init__(self):
        self._config = None
    
    def load_config(self, env_file_path=None):
        # Load from .env file or use defaults
        telegram_token = os.getenv("TELEGRAM_TOKEN", "demo_token")
        openai_api_key = os.getenv("OPENAI_API_KEY", "demo_key")
        firestore_credentials_path = os.getenv("FIRESTORE_CREDENTIALS_PATH", "secrets/firebase-credentials.json")
        log_level = os.getenv("LOG_LEVEL", "DEBUG")
        
        self._config = Config(
            telegram_token=telegram_token,
            openai_api_key=openai_api_key,
            firestore_credentials_path=firestore_credentials_path,
            log_level=log_level
        )
        return self._config

# Simplified UserProfileDTO class
class UserProfileDTO:
    def __init__(self, telegram_id, username=None, first_name=None, last_name=None):
        self.id = None
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.registration_date = datetime.now()
        self.goals = {}

# Simplified MealDTO class
class MealDTO:
    def __init__(self, user_id, food_name, calories, proteins, fats, carbs, meal_type="snack"):
        self.id = None
        self.user_id = user_id
        self.timestamp = datetime.now()
        self.meal_type = meal_type
        self.food_name = food_name
        self.calories = calories
        self.proteins = proteins
        self.fats = fats
        self.carbs = carbs
        self.image_url = None

# Mock TelegramService
class TelegramService:
    def __init__(self, config):
        self.config = config
        logger.info("TelegramService initialized with token: %s", config.telegram_token[:4] + "...")
    
    async def send_message(self, chat_id, text):
        logger.info("[TELEGRAM] Message to %s: %s", chat_id, text)
        return True

# Mock OpenAIService
class OpenAIService:
    def __init__(self, config):
        self.config = config
        logger.info("OpenAIService initialized with key: %s", config.openai_api_key[:4] + "...")
    
    async def analyze_food_image(self, image_path):
        logger.info("[OPENAI] Analyzing image: %s", image_path)
        # Return mock analysis
        return {
            "success": True,
            "food_name": "Chicken Salad",
            "calories": 350.5,
            "proteins": 25.3,
            "fats": 15.2,
            "carbs": 10.7
        }

# Mock FirestoreService
class FirestoreService:
    def __init__(self, config):
        self.config = config
        self.users = {}
        self.meals = {}
        logger.info("FirestoreService initialized with credentials: %s", config.firestore_credentials_path)
    
    def save_user(self, user_profile):
        user_id = f"user-{user_profile.telegram_id}"
        self.users[user_id] = {
            "telegram_id": user_profile.telegram_id,
            "username": user_profile.username,
            "first_name": user_profile.first_name,
            "last_name": user_profile.last_name,
            "registration_date": user_profile.registration_date,
            "goals": user_profile.goals
        }
        logger.info("[FIRESTORE] Saved user: %s", user_id)
        return user_id
    
    def save_meal(self, meal):
        meal_id = f"meal-{len(self.meals) + 1}"
        self.meals[meal_id] = {
            "user_id": meal.user_id,
            "timestamp": meal.timestamp,
            "meal_type": meal.meal_type,
            "food_name": meal.food_name,
            "calories": meal.calories,
            "proteins": meal.proteins,
            "fats": meal.fats,
            "carbs": meal.carbs,
            "image_url": meal.image_url
        }
        logger.info("[FIRESTORE] Saved meal: %s", meal_id)
        return meal_id

# Simplified demo to simulate a user sending a photo
async def run_demo():
    # Load configuration
    logger.info("Starting Food Tracking Bot Demo...")
    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    # Initialize services
    telegram_service = TelegramService(config)
    openai_service = OpenAIService(config)
    firestore_service = FirestoreService(config)
    
    # Simulate user registration
    user = UserProfileDTO(
        telegram_id=123456789,
        username="test_user",
        first_name="Test",
        last_name="User"
    )
    user_id = firestore_service.save_user(user)
    logger.info("Registered user with ID: %s", user_id)
    
    # Simulate receiving a photo
    logger.info("Receiving photo from user...")
    
    # Simulate photo path
    photo_path = "temp/test_food.jpg"
    
    # Create a test image if it doesn't exist
    if not os.path.exists(photo_path):
        with open(photo_path, "w") as f:
            f.write("This is a placeholder for an image file")
    
    # Analyze photo
    logger.info("Analyzing photo...")
    analysis_result = await openai_service.analyze_food_image(photo_path)
    
    # Save meal data
    meal = MealDTO(
        user_id=user_id,
        food_name=analysis_result["food_name"],
        calories=analysis_result["calories"],
        proteins=analysis_result["proteins"],
        fats=analysis_result["fats"],
        carbs=analysis_result["carbs"],
        meal_type="lunch"
    )
    meal_id = firestore_service.save_meal(meal)
    logger.info("Saved meal with ID: %s", meal_id)
    
    # Send response to user
    response = (
        f"✅ Результаты анализа:\n\n"
        f"🍽 {meal.food_name}\n\n"
        f"🔥 Калории: {meal.calories} ккал\n"
        f"🥩 Белки: {meal.proteins} г\n"
        f"🧈 Жиры: {meal.fats} г\n"
        f"🍚 Углеводы: {meal.carbs} г\n\n"
        f"Прием пищи сохранен как: Обед"
    )
    
    await telegram_service.send_message(user.telegram_id, response)
    
    logger.info("Demo completed successfully!")

# Run the demo
if __name__ == "__main__":
    # Check if we can import asyncio
    try:
        import asyncio
        asyncio.run(run_demo())
    except ImportError:
        logger.error("asyncio not available, cannot run demo")
        print("Please install a compatible Python version (3.7+) that supports asyncio")