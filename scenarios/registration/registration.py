from typing import Dict, Any
from loguru import logger

from scenarios.base import AbstractScenario
from dto.profile import UserProfileDTO
from core.localization import i18n


class RegistrationScenario(AbstractScenario):
    """Scenario for user registration."""
    
    def __init__(self, user_service, telegram_service):
        """
        Initialize the registration scenario.
        
        Args:
            user_service: User service for saving user data
            telegram_service: Telegram service for sending messages
        """
        self.user_service = user_service
        self.telegram_service = telegram_service
    
    async def start(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start the registration scenario.
        
        Args:
            context (Dict[str, Any]): Context including telegram_user and chat_id
            
        Returns:
            Dict[str, Any]: Updated context
        """
        logger.info(f"Starting registration scenario for user: {context['telegram_user']['id']}")
        
        # Get data from context
        telegram_user = context["telegram_user"]
        chat_id = context["chat_id"]
        user_language = context.get("user_language")
        reply_to_message_id = context.get("reply_to_message_id")
        
        # Check if user is already registered
        existing_user = self.user_service.get_user(telegram_user["id"])
        
        if existing_user:
            # User already exists
            welcome_back_msg = i18n.gettext(
                "Добро пожаловать обратно, %name%! Я готов помочь вам с анализом питания.",
                user_language,
                {"name": telegram_user['first_name']}
            )
            await self.telegram_service.send_message(chat_id, welcome_back_msg, reply_to_message_id=reply_to_message_id)
            
            # Set scenario as completed
            context["completed"] = True
            logger.info(f"User {telegram_user['id']} already registered, skipping registration")
            
            return context
        
        # Create user profile
        user_profile = UserProfileDTO(
            telegram_id=telegram_user["id"],
            username=telegram_user.get("username"),
            first_name=telegram_user.get("first_name"),
            last_name=telegram_user.get("last_name")
        )
        
        # Save user profile
        user_id = self.user_service.create_user(user_profile)
        
        # Update context
        context["user_id"] = user_id
        context["step"] = "welcome"
        context["completed"] = False
        
        # Send welcome message
        welcome_parts = [
            i18n.gettext("👋 Добро пожаловать, %name%!", user_language, {"name": telegram_user['first_name']}),
            "",
            i18n.gettext("Я бот для анализа питания. Отправьте мне фотографию еды, и я помогу определить её калорийность и пищевую ценность.", user_language),
            "",
            i18n.gettext("Вы можете использовать следующие команды:", user_language),
            i18n.gettext("/stats - Посмотреть статистику вашего питания", user_language)
        ]
        
        welcome_message = "\n".join(welcome_parts)
        
        await self.telegram_service.send_message(chat_id, welcome_message, reply_to_message_id=reply_to_message_id)
        
        # Mark scenario as completed
        context["completed"] = True
        logger.info(f"Registration completed for user {telegram_user['id']}")
        
        return context
    
    async def next_step(self, context: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the next step in the scenario.
        
        Args:
            context (Dict[str, Any]): Current scenario context
            input_data (Dict[str, Any]): Input data from the user
            
        Returns:
            Dict[str, Any]: Updated context
        """
        # Since we're keeping registration simple, we complete it in one step
        # This method is included to fulfill the abstract class contract
        
        if context.get("completed", False):
            # Scenario is already completed
            return context
        
        # Mark as completed (fallback)
        context["completed"] = True
        return context
    
    async def cancel(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cancel the registration scenario.
        
        Args:
            context (Dict[str, Any]): Current scenario context
            
        Returns:
            Dict[str, Any]: Final context after cancellation
        """
        chat_id = context["chat_id"]
        user_language = context.get("user_language")
        
        await self.telegram_service.send_message(
            chat_id,
            i18n.gettext("Регистрация отменена. Вы можете начать снова, отправив команду /start.", user_language),
            reply_to_message_id=context.get("reply_to_message_id")
        )
        
        context["completed"] = True
        logger.info(f"Registration cancelled for user {context['telegram_user']['id']}")
        
        return context