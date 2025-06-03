import os
from typing import Optional
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import InputFile, Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
from loguru import logger

from config.config import Config
from core.localization import i18n


class TelegramService:
    """Service for interacting with Telegram Bot API."""
    
    def __init__(self, config: Config):
        """
        Initialize the Telegram service.
        
        Args:
            config (Config): Application configuration
        """
        self.config = config
        self.bot = Bot(token=config.telegram_token)
        self.dp = Dispatcher()
        self.router = Router()
        self._scenario_orchestrator = None
        logger.info("Telegram service initialized")
    
    def set_orchestrator(self, orchestrator):
        """
        Set the scenario orchestrator.
        
        Args:
            orchestrator: The scenario orchestrator
        """
        self._scenario_orchestrator = orchestrator
    
    async def setup_handlers(self):
        """Set up message handlers."""
        # Command handlers
        self.router.message.register(self._handle_start, Command(commands=['start', 'help']))
        self.router.message.register(self._handle_stats, Command(commands=['stats']))
        
        # Photo handler
        self.router.message.register(self._handle_photo, F.photo)
        
        # Text message handler (catches all text messages)
        self.router.message.register(self._handle_message, F.text)
        
        # Include router in dispatcher
        self.dp.include_router(self.router)
        
        logger.info("Telegram handlers set up")
    
    async def start_polling(self):
        """Start the bot in polling mode."""
        logger.info("Starting Telegram bot in polling mode")
        await self.dp.start_polling(self.bot)
    
    async def setup_webhook(self, webhook_url: str, webhook_path: str):
        """
        Set up webhook for the bot.
        
        Args:
            webhook_url (str): Webhook URL
            webhook_path (str): Webhook path
        """
        await self.bot.set_webhook(url=webhook_url + webhook_path)
        logger.info(f"Webhook set up at {webhook_url + webhook_path}")
    
    async def send_message(self, chat_id: int, text: str, parse_mode: Optional[str] = ParseMode.HTML, reply_to_message_id: Optional[int] = None):
        """
        Send a text message to a chat.
        
        Args:
            chat_id (int): Telegram chat ID
            text (str): Message text
            parse_mode (Optional[str]): Message parse mode
            reply_to_message_id (Optional[int]): Message ID to reply to
        """
        await self.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, reply_to_message_id=reply_to_message_id)
        logger.debug(f"Message sent to chat_id: {chat_id}")
    
    async def send_photo(self, chat_id: int, photo_path: str, caption: Optional[str] = None):
        """
        Send a photo to a chat.
        
        Args:
            chat_id (int): Telegram chat ID
            photo_path (str): Path to the photo file
            caption (Optional[str]): Photo caption
        """
        with open(photo_path, 'rb') as photo:
            await self.bot.send_photo(
                chat_id=chat_id,
                photo=InputFile(photo),
                caption=caption
            )
        logger.debug(f"Photo sent to chat_id: {chat_id}")
    
    async def _handle_start(self, message: Message):
        """
        Handle /start and /help commands.
        
        Args:
            message (Message): Telegram message
        """
        user_id = message.from_user.id
        chat_id = message.chat.id
        user_language = message.from_user.language_code
        
        if self._scenario_orchestrator:
            # Start registration scenario if user is new
            context = {
                "telegram_user": message.from_user.model_dump(),
                "chat_id": chat_id,
                "user_language": user_language,
                "reply_to_message_id": message.message_id
            }
            
            await self._scenario_orchestrator.start_scenario("registration", user_id, context)
        else:
            welcome_text = i18n.gettext(
                "👋 Добро пожаловать в бот для отслеживания питания!\n\n"
                "Отправьте мне фотографию еды, и я помогу определить её калорийность и пищевую ценность.",
                user_language
            )
            await self.send_message(chat_id, welcome_text, reply_to_message_id=message.message_id)
    
    async def _handle_stats(self, message: Message):
        """
        Handle /stats command.
        
        Args:
            message (Message): Telegram message
        """
        user_id = message.from_user.id
        chat_id = message.chat.id
        user_language = message.from_user.language_code
        
        if self._scenario_orchestrator:
            # Start stats scenario
            context = {
                "telegram_user": message.from_user.model_dump(),
                "chat_id": chat_id,
                "user_language": user_language,
                "reply_to_message_id": message.message_id
            }
            
            await self._scenario_orchestrator.start_scenario("stats", user_id, context)
        else:
            await self.send_message(chat_id, i18n.gettext("Статистика временно недоступна.", user_language), reply_to_message_id=message.message_id)
    
    async def _handle_photo(self, message: Message):
        """
        Handle photo messages.
        
        Args:
            message (Message): Telegram message with photo
        """
        user_id = message.from_user.id
        chat_id = message.chat.id
        user_language = message.from_user.language_code
        
        # Get the largest photo available
        photo = message.photo[-1]
        file_id = photo.file_id
        
        # Download the photo
        file_info = await self.bot.get_file(file_id)
        file_path = file_info.file_path
        download_path = f"temp/{file_id}.jpg"
        
        # Create temp directory if it doesn't exist
        os.makedirs("temp", exist_ok=True)
        
        await self.bot.download_file(file_path, download_path)
        
        if self._scenario_orchestrator:
            # Start meal photo scenario
            context = {
                "telegram_user": message.from_user.model_dump(),
                "chat_id": chat_id,
                "photo_path": download_path,
                "user_language": user_language,
                "reply_to_message_id": message.message_id
            }
            
            await self._scenario_orchestrator.start_scenario("meal_photo", user_id, context)
        else:
            await self.send_message(chat_id, i18n.gettext("Получил вашу фотографию, но анализ временно недоступен.", user_language), reply_to_message_id=message.message_id)
    
    async def _handle_message(self, message: Message):
        """
        Handle text messages.
        
        Args:
            message (Message): Telegram message
        """
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        user_language = message.from_user.language_code
        
        if self._scenario_orchestrator:
            # Process message through active scenario if exists
            update_data = {
                "message_type": "text",
                "text": text,
                "user_language": user_language,
                "reply_to_message_id": message.message_id
            }
            
            await self._scenario_orchestrator.process_update(user_id, update_data)
        else:
            await self.send_message(
                chat_id, 
                i18n.gettext("Отправьте мне фотографию еды, и я помогу определить её калорийность и пищевую ценность.", user_language),
                reply_to_message_id=message.message_id
            )