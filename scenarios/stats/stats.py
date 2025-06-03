from typing import Dict, Any
from loguru import logger

from scenarios.base import AbstractScenario
from core.localization import i18n


class StatsScenario(AbstractScenario):
    """Scenario for showing user statistics."""
    
    def __init__(self, meal_service, telegram_service):
        """
        Initialize the stats scenario.
        
        Args:
            meal_service: Service for retrieving meal data
            telegram_service: Service for sending messages
        """
        self.meal_service = meal_service
        self.telegram_service = telegram_service
    
    async def start(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start the stats scenario.
        
        Args:
            context (Dict[str, Any]): Context including telegram_user and chat_id
            
        Returns:
            Dict[str, Any]: Updated context
        """
        logger.info(f"Starting stats scenario for user: {context['telegram_user']['id']}")
        
        # Get data from context
        telegram_user = context["telegram_user"]
        chat_id = context["chat_id"]
        user_language = context.get("user_language")
        reply_to_message_id = context.get("reply_to_message_id")
        
        # For now, just send a simple message
        stats_message = i18n.gettext(
            "📊 Статистика временно недоступна.\n\n"
            "В будущих версиях здесь будет отображаться ваша статистика питания.",
            user_language
        )
        
        await self.telegram_service.send_message(
            chat_id, 
            stats_message,
            reply_to_message_id=reply_to_message_id
        )
        
        # Mark scenario as completed
        context["completed"] = True
        logger.info(f"Stats scenario completed for user {telegram_user['id']}")
        
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
        # Stats scenario is completed in one step
        if context.get("completed", False):
            return context
        
        # Mark as completed (fallback)
        context["completed"] = True
        return context
    
    async def cancel(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cancel the stats scenario.
        
        Args:
            context (Dict[str, Any]): Current scenario context
            
        Returns:
            Dict[str, Any]: Final context after cancellation
        """
        chat_id = context["chat_id"]
        user_language = context.get("user_language")
        
        await self.telegram_service.send_message(
            chat_id,
            i18n.gettext("Просмотр статистики отменён.", user_language),
            reply_to_message_id=context.get("reply_to_message_id")
        )
        
        context["completed"] = True
        logger.info(f"Stats scenario cancelled for user {context['telegram_user']['id']}")
        
        return context