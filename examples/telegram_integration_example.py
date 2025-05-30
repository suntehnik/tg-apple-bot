"""
Example of integrating the localization service with the TelegramService.
This shows how to modify the TelegramService to use localization.
"""
import asyncio
from typing import Dict, Any, Optional
from aiogram.enums import ParseMode
from loguru import logger

from config.config import Config
from core.localization import get

class LocalizedTelegramService:
    """
    Example of a TelegramService with localization integration.
    This is a simplified version showing just the relevant methods.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the service.
        In a real implementation, this would initialize the actual Telegram bot.
        """
        self.config = config
        logger.info("Localized Telegram service initialized")
    
    async def send_message(self, chat_id: int, key: str, params: Optional[Dict[str, Any]] = None, 
                           user_locale: Optional[str] = None, parse_mode: Optional[str] = ParseMode.HTML):
        """
        Send a localized text message to a chat.
        
        Args:
            chat_id (int): Telegram chat ID
            key (str): Message key (original Russian text)
            params (Optional[Dict[str, Any]]): Parameters for string formatting
            user_locale (Optional[str]): User's Telegram locale
            parse_mode (Optional[str]): Message parse mode
        """
        # Get localized text
        localized_text = get(key, user_locale, params)
        
        # In a real implementation, this would call the actual Telegram API
        logger.debug(f"Sending localized message to chat_id: {chat_id}")
        print(f"SEND TO CHAT {chat_id}: {localized_text}")
    
    async def _handle_start(self, message: Dict[str, Any]):
        """
        Handle /start and /help commands with localization.
        
        Args:
            message: Telegram message (simplified)
        """
        user_id = message["from"]["id"]
        chat_id = message["chat"]["id"]
        user_locale = message["from"].get("language_code")
        
        welcome_text = "Добро пожаловать! Давайте начнем регистрацию."
        
        # Send localized welcome message
        await self.send_message(chat_id, welcome_text, user_locale=user_locale)

async def simulate_interaction():
    """Simulate a user interaction with the bot."""
    # Create a simple config
    config = Config(
        telegram_token="fake_token",
        openai_api_key="fake_key",
        firestore_credentials_path="fake_path"
    )
    
    # Create the localized service
    service = LocalizedTelegramService(config)
    
    # Simulate a message from a Russian user
    russian_message = {
        "from": {"id": 123, "language_code": "ru"},
        "chat": {"id": 123}
    }
    
    # Simulate a message from an English user
    english_message = {
        "from": {"id": 456, "language_code": "en"},
        "chat": {"id": 456}
    }
    
    # Handle start command for both users
    await service._handle_start(russian_message)
    await service._handle_start(english_message)
    
    # Example of sending a parameterized message
    meal_result_key = "Обнаружено блюдо: %dish_name%"
    meal_params = {"dish_name": "Пицца"}
    
    await service.send_message(
        chat_id=123,
        key=meal_result_key, 
        params=meal_params, 
        user_locale="ru"
    )
    
    await service.send_message(
        chat_id=456,
        key=meal_result_key, 
        params=meal_params, 
        user_locale="en"
    )

async def main():
    await simulate_interaction()

if __name__ == "__main__":
    asyncio.run(main())