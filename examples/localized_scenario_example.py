"""
Example of refactoring a scenario to use localization.
This shows how the MealPhotoScenario could be modified to use the localization service.
"""
import os
from typing import Dict, Any
from loguru import logger

from scenarios.base import AbstractScenario
from dto.meal import MealDTO
from core.localization import get


class LocalizedMealPhotoScenario(AbstractScenario):
    """Localized version of the meal photo scenario."""
    
    def __init__(self, food_analysis_service, meal_service, telegram_service):
        """
        Initialize the meal photo scenario.
        
        Args:
            food_analysis_service: Service for analyzing food images
            meal_service: Service for saving meal data
            telegram_service: Service for sending messages
        """
        self.food_analysis_service = food_analysis_service
        self.meal_service = meal_service
        self.telegram_service = telegram_service
    
    async def start(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start the meal photo scenario with localization.
        
        Args:
            context (Dict[str, Any]): Context including photo_path, telegram_user, chat_id
            
        Returns:
            Dict[str, Any]: Updated context
        """
        logger.info(f"Starting meal photo scenario for user: {context['telegram_user']['id']}")
        
        # Get data from context
        telegram_user = context["telegram_user"]
        chat_id = context["chat_id"]
        photo_path = context["photo_path"]
        user_locale = telegram_user.get("language_code")
        
        # Check if photo exists
        if not os.path.exists(photo_path):
            error_msg = "Произошла ошибка при обработке фотографии. Пожалуйста, попробуйте снова."
            await self.telegram_service.send_message(chat_id, get(error_msg, user_locale))
            
            context["completed"] = True
            logger.error(f"Photo not found: {photo_path}")
            return context
        
        # Send processing message
        processing_msg = "🔍 Анализирую вашу фотографию еды... Это может занять несколько секунд."
        await self.telegram_service.send_message(chat_id, get(processing_msg, user_locale))
        
        # Analyze the image
        analysis_result = await self.food_analysis_service.analyze_image(photo_path)
        
        if not analysis_result.get("success", False):
            # Analysis failed
            error_message = analysis_result.get("error", "Неизвестная ошибка")
            error_template = "Не удалось проанализировать изображение: %error%\n" \
                            "Пожалуйста, попробуйте другую фотографию с более четким изображением еды."
            
            await self.telegram_service.send_message(
                chat_id,
                get(error_template, user_locale, {"error": error_message})
            )
            
            context["completed"] = True
            logger.error(f"Food analysis failed: {error_message}")
            return context
        
        # Format analysis results
        food_name = analysis_result.get("food_name", "Неизвестное блюдо")
        calories = analysis_result.get("calories", 0)
        proteins = analysis_result.get("proteins", 0)
        fats = analysis_result.get("fats", 0)
        carbs = analysis_result.get("carbs", 0)
        
        # Update context with analysis results
        context["analysis_result"] = analysis_result
        context["step"] = "confirm"
        
        # Prepare meal DTO (we'll save it after confirmation)
        meal = MealDTO(
            user_id=str(telegram_user["id"]), # convert to string
            food_name=food_name,
            calories=calories,
            proteins=proteins,
            fats=fats,
            carbs=carbs,
            meal_type="snack"  # Default meal type
        )
        
        context["meal"] = meal.model_dump()
        
        # Send analysis results with localization
        dish_detected = get("Обнаружено блюдо: %dish_name%", user_locale, {"dish_name": food_name})
        calories_text = get("Калории: %calories% ккал", user_locale, {"calories": calories})
        protein_text = get("Белки: %protein% г", user_locale, {"protein": proteins})
        fat_text = get("Жиры: %fat% г", user_locale, {"fat": fats})
        carbs_text = get("Углеводы: %carbs% г", user_locale, {"carbs": carbs})
        
        # Hard-coded for simplicity in this example
        # In a real implementation, these would also be localized
        meal_types_prompt = get(
            "Выберите тип приема пищи:\n1. Завтрак\n2. Обед\n3. Ужин\n4. Перекус (по умолчанию)\n\n" \
            "Отправьте номер или название типа приема пищи.",
            user_locale
        )
        
        result_message = (
            f"✅ {get('Результаты анализа:', user_locale)}\n\n"
            f"🍽 <b>{dish_detected}</b>\n\n"
            f"🔥 {calories_text}\n"
            f"🥩 {protein_text}\n"
            f"🧈 {fat_text}\n"
            f"🍚 {carbs_text}\n\n"
            f"{meal_types_prompt}"
        )
        
        await self.telegram_service.send_message(chat_id, result_message)
        
        return context

    # The rest of the scenario methods would also be updated to use localization
    # For brevity, only the start method is shown in this example


# Example usage in app.py:
"""
# Initialize localization
from core.localization import init
init()  # Load locales from default directory

# Then proceed with normal initialization
telegram_service = TelegramService(config)
...
"""