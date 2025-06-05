import os
import asyncio
from loguru import logger

from config.config_manager import ConfigManager
from core.logging.logger import Logger
from core.services.telegram import TelegramService
from core.services.firestore import FirestoreService
from core.services.openai import OpenAIService
from scenarios.orchestrator import ScenarioOrchestrator
from scenarios.registration.registration import RegistrationScenario
from scenarios.meal.meal_photo import MealPhotoScenario
from scenarios.stats.stats import StatsScenario
from services.user_service import UserService
from services.meal_service import MealService
from services.food_analysis import FoodAnalysisService
from core.localization import i18n

async def setup_app():
    """Set up and initialize the application."""
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("temp", exist_ok=True)
    
    # Load configuration
    config_manager = ConfigManager()
    config = config_manager.load_config(env_file_path=".env")
    
    # Set up logging
    Logger.setup(config.log_level)
    logger.info("Starting Food Tracking Bot...")
    
    i18n.init(default_language="it")
    
    # Initialize services
    telegram_service = TelegramService(config)
    firestore_service = FirestoreService(config)
    openai_service = OpenAIService(config)
    
    # Initialize business services
    user_service = UserService(firestore_service)
    meal_service = MealService(firestore_service)
    food_analysis_service = FoodAnalysisService(openai_service)
    
    # Initialize scenarios
    orchestrator = ScenarioOrchestrator()
    
    # Register scenarios
    registration_scenario = RegistrationScenario(user_service, telegram_service)
    meal_photo_scenario = MealPhotoScenario(food_analysis_service, meal_service, telegram_service)
    stats_scenario = StatsScenario(meal_service, telegram_service)
    
    orchestrator.register_scenario("registration", registration_scenario)
    orchestrator.register_scenario("meal_photo", meal_photo_scenario)
    orchestrator.register_scenario("stats", stats_scenario)
    
    # Set orchestrator in telegram service
    telegram_service.set_orchestrator(orchestrator)
    
    # Set up message handlers
    await telegram_service.setup_handlers()
    
    return telegram_service


async def main():
    """Main application entry point."""
    telegram_service = await setup_app()
    
    try:
        logger.info("Starting telegram bot...")
        await telegram_service.start_polling()
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
    finally:
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())