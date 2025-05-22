import os
from typing import Dict, Any
from loguru import logger

from scenarios.base import AbstractScenario
from dto.meal import MealDTO


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
        
        # Check if photo exists
        if not os.path.exists(photo_path):
            await self.telegram_service.send_message(
                chat_id,
                "Произошла ошибка при обработке фотографии. Пожалуйста, попробуйте снова."
            )
            
            context["completed"] = True
            logger.error(f"Photo not found: {photo_path}")
            return context
        
        # Send processing message
        await self.telegram_service.send_message(
            chat_id,
            "🔍 Анализирую вашу фотографию еды... Это может занять несколько секунд."
        )
        
        # Analyze the image
        analysis_result = await self.food_analysis_service.analyze_image(photo_path)
        
        if not analysis_result.get("success", False):
            # Analysis failed
            error_message = analysis_result.get("error", "Неизвестная ошибка")
            await self.telegram_service.send_message(
                chat_id,
                f"Не удалось проанализировать изображение: {error_message}\n"
                "Пожалуйста, попробуйте другую фотографию с более четким изображением еды."
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
        
        # Send analysis results
        result_message = (
            f"✅ Результаты анализа:\n\n"
            f"🍽 <b>{food_name}</b>\n\n"
            f"🔥 Калории: <b>{calories} ккал</b>\n"
            f"🥩 Белки: <b>{proteins} г</b>\n"
            f"🧈 Жиры: <b>{fats} г</b>\n"
            f"🍚 Углеводы: <b>{carbs} г</b>\n\n"
            f"Выберите тип приема пищи:\n"
            f"1. Завтрак\n"
            f"2. Обед\n"
            f"3. Ужин\n"
            f"4. Перекус (по умолчанию)\n\n"
            f"Отправьте номер или название типа приема пищи."
        )
        
        await self.telegram_service.send_message(chat_id, result_message)
        
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
        
        if step == "confirm":
            # Process meal type selection
            if input_data.get("message_type") == "text":
                text = input_data.get("text", "").lower()
                meal_type = "snack"  # Default
                
                # Determine meal type from input
                if text in ["1", "завтрак"]:
                    meal_type = "breakfast"
                elif text in ["2", "обед"]:
                    meal_type = "lunch"
                elif text in ["3", "ужин"]:
                    meal_type = "dinner"
                elif text in ["4", "перекус"]:
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
                    "breakfast": "Завтрак",
                    "lunch": "Обед",
                    "dinner": "Ужин",
                    "snack": "Перекус"
                }
                
                meal_type_name = meal_type_names.get(meal_type, "Прием пищи")
                
                confirmation_message = (
                    f"✅ {meal_type_name} успешно добавлен!\n\n"
                    f"🍽 <b>{meal.food_name}</b>\n"
                    f"🔥 Калории: <b>{meal.calories} ккал</b>\n"
                    f"🥩 Белки: <b>{meal.proteins} г</b>\n"
                    f"🧈 Жиры: <b>{meal.fats} г</b>\n"
                    f"🍚 Углеводы: <b>{meal.carbs} г</b>\n\n"
                    f"Отправьте мне еще одну фотографию еды для анализа."
                )
                
                await self.telegram_service.send_message(chat_id, confirmation_message)
                
                # Clean up temporary photo file
                if "photo_path" in context and os.path.exists(context["photo_path"]):
                    os.remove(context["photo_path"])
                    logger.debug(f"Removed temporary photo: {context['photo_path']}")
            
            else:
                # Invalid input
                await self.telegram_service.send_message(
                    chat_id,
                    "Пожалуйста, выберите тип приема пищи, отправив номер от 1 до 4."
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
        
        await self.telegram_service.send_message(
            chat_id,
            "❌ Добавление приема пищи отменено."
        )
        
        # Clean up temporary photo file
        if "photo_path" in context and os.path.exists(context["photo_path"]):
            os.remove(context["photo_path"])
            logger.debug(f"Removed temporary photo: {context['photo_path']}")
        
        context["completed"] = True
        logger.info(f"Meal photo scenario cancelled for user {context['telegram_user']['id']}")
        
        return context