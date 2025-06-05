import os
from typing import Dict, Any
from loguru import logger

from scenarios.base import AbstractScenario
from dto.meal import MealDTO
from core.localization import i18n


class MealPhotoScenario(AbstractScenario):
    """Scenario for adding a meal photo."""
    
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
        Start the meal photo scenario.
        
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
        user_language = context.get("user_language")
        reply_to_message_id = context.get("reply_to_message_id")
        
        # Check if photo exists
        if not os.path.exists(photo_path):
            await self.telegram_service.send_message(
                chat_id,
                i18n.gettext("Произошла ошибка при обработке фотографии. Пожалуйста, попробуйте снова.", user_language),
                reply_to_message_id=reply_to_message_id
            )
            
            context["completed"] = True
            logger.error(f"Photo not found: {photo_path}")
            return context
        
        # Send processing message
        await self.telegram_service.send_message(
            chat_id,
            i18n.gettext("🔍 Анализирую вашу фотографию еды... Это может занять несколько секунд.", user_language),
            reply_to_message_id=reply_to_message_id
        )
        
        # Analyze the image
        analysis_result = await self.food_analysis_service.analyze_image(photo_path)
        
        if not analysis_result.get("success", False):
            # Analysis failed
            error_message = analysis_result.get("error", "Неизвестная ошибка")
            await self.telegram_service.send_message(
                chat_id,
                i18n.gettext(
                    "Не удалось проанализировать изображение: %error_message%\n"
                    "Пожалуйста, попробуйте другую фотографию с более четким изображением еды.",
                    user_language,
                    {"error_message": error_message}
                ),
                reply_to_message_id=reply_to_message_id
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
        
        # Send analysis results - using localized strings
        result_message_parts = [
            i18n.gettext("✅ Результаты анализа:", user_language),
            "",
            f"🍽 <b>{food_name}</b>",
            "",
            i18n.gettext("🔥 Калории: %calories% ккал", user_language, {"calories": calories}),
            i18n.gettext("🥩 Белки: %proteins% г", user_language, {"proteins": proteins}),
            i18n.gettext("🧈 Жиры: %fats% г", user_language, {"fats": fats}),
            i18n.gettext("🍚 Углеводы: %carbs% г", user_language, {"carbs": carbs}),
            "",
            i18n.gettext("Выберите тип приема пищи:", user_language),
            i18n.gettext("1. Завтрак", user_language),
            i18n.gettext("2. Обед", user_language),
            i18n.gettext("3. Ужин", user_language),
            i18n.gettext("4. Перекус (по умолчанию)", user_language),
            "",
            i18n.gettext("Отправьте номер или название типа приема пищи.", user_language)
        ]
        
        result_message = "\n".join(result_message_parts)
        await self.telegram_service.send_message(chat_id, result_message, reply_to_message_id=reply_to_message_id)
        
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
        # Get data from context
        telegram_user = context["telegram_user"]
        chat_id = context["chat_id"]
        step = context.get("step", "confirm")
        user_language = context.get("user_language") or input_data.get("user_language")
        reply_to_message_id = input_data.get("reply_to_message_id")
        
        if step == "confirm":
            # Process meal type selection
            if input_data.get("message_type") == "text":
                text = input_data.get("text", "").lower()
                meal_type = "snack"  # Default
                
                # Determine meal type from input
                if text in ["1", i18n.gettext("завтрак", user_language).lower()]:
                    meal_type = "breakfast"
                elif text in ["2", i18n.gettext("обед", user_language).lower()]:
                    meal_type = "lunch"
                elif text in ["3", i18n.gettext("ужин", user_language).lower()]:
                    meal_type = "dinner"
                elif text in ["4", i18n.gettext("перекус", user_language).lower()]:
                    meal_type = "snack"
                
                # Update meal type
                context["meal"]["meal_type"] = meal_type
                
                # Create and save meal
                meal = MealDTO(**context["meal"])
                meal_id = self.meal_service.add_meal(telegram_user["id"], meal)
                
                # Update context
                context["meal_id"] = meal_id
                context["step"] = "completed"
                context["completed"] = True
                
                # Send confirmation message  
                meal_type_names = {
                    "breakfast": i18n.gettext("Завтрак", user_language),
                    "lunch": i18n.gettext("Обед", user_language),
                    "dinner": i18n.gettext("Ужин", user_language),
                    "snack": i18n.gettext("Перекус", user_language)
                }
                
                meal_type_name = meal_type_names.get(meal_type, i18n.gettext("Прием пищи", user_language))
                
                confirmation_parts = [
                    i18n.gettext("✅ %meal_type% успешно добавлен!", user_language, {"meal_type": meal_type_name}),
                    "",
                    f"🍽 <b>{meal.food_name}</b>",
                    i18n.gettext("🔥 Калории: %calories% ккал", user_language, {"calories": meal.calories}),
                    i18n.gettext("🥩 Белки: %proteins% г", user_language, {"proteins": meal.proteins}),
                    i18n.gettext("🧈 Жиры: %fats% г", user_language, {"fats": meal.fats}),
                    i18n.gettext("🍚 Углеводы: %carbs% г", user_language, {"carbs": meal.carbs}),
                    "",
                    i18n.gettext("Отправьте мне еще одну фотографию еды для анализа.", user_language)
                ]
                
                confirmation_message = "\n".join(confirmation_parts)
                
                await self.telegram_service.send_message(chat_id, confirmation_message, reply_to_message_id=reply_to_message_id)
                
                # Clean up temporary photo file
                if "photo_path" in context and os.path.exists(context["photo_path"]):
                    os.remove(context["photo_path"])
                    logger.debug(f"Removed temporary photo: {context['photo_path']}")
            
            else:
                # Invalid input
                await self.telegram_service.send_message(
                    chat_id,
                    i18n.gettext("Пожалуйста, выберите тип приема пищи, отправив номер от 1 до 4.", user_language),
                    reply_to_message_id=reply_to_message_id
                )
        
        return context
    
    async def cancel(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cancel the meal photo scenario.
        
        Args:
            context (Dict[str, Any]): Current scenario context
            
        Returns:
            Dict[str, Any]: Final context after cancellation
        """
        chat_id = context["chat_id"]
        user_language = context.get("user_language")
        
        await self.telegram_service.send_message(
            chat_id,
            i18n.gettext("❌ Добавление приема пищи отменено.", user_language),
            reply_to_message_id=context.get("reply_to_message_id")
        )
        
        # Clean up temporary photo file
        if "photo_path" in context and os.path.exists(context["photo_path"]):
            os.remove(context["photo_path"])
            logger.debug(f"Removed temporary photo: {context['photo_path']}")
        
        context["completed"] = True
        logger.info(f"Meal photo scenario cancelled for user {context['telegram_user']['id']}")
        
        return context