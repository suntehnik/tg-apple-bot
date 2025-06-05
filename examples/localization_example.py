"""
Example of using the localization service in a Telegram bot.
This shows how to use the localization service to translate strings based on user's locale.
"""
import asyncio
from core.localization import init, get

# Sample Telegram update object (simplified)
telegram_user = {
    "id": 123456789,
    "language_code": "en",  # This is the user's Telegram locale
    "username": "example_user"
}

# Simulate sending a message to a user with the appropriate language
async def send_localized_message(chat_id, key, params=None, user_locale=None):
    """
    Simulate sending a localized message to a user.
    
    Args:
        chat_id: Telegram chat ID
        key: Message key (original Russian text)
        params: Optional parameters for string formatting
        user_locale: User's Telegram locale
    """
    localized_text = get(key, user_locale, params)
    print(f"Sending to chat {chat_id}: {localized_text}")
    # In a real application, you would call telegram_service.send_message here

async def main():
    # Initialize the localization service
    init()
    print("Localization service initialized")
    
    # Example 1: Basic message localization
    russian_user = {"language_code": "ru"}
    english_user = {"language_code": "en"}
    
    message_key = "Привет! Я бот для отслеживания питания."
    
    await send_localized_message(123, message_key, user_locale=russian_user["language_code"])
    await send_localized_message(456, message_key, user_locale=english_user["language_code"])
    
    # Example 2: Message with parameters
    name_message_key = "Спасибо, %name%! Какой у вас рост (в см)?"
    params = {"name": "John"}
    
    await send_localized_message(123, name_message_key, params, russian_user["language_code"])
    await send_localized_message(456, name_message_key, params, english_user["language_code"])
    
    # Example 3: Meal analysis results with parameters
    meal_result_key = "Обнаружено блюдо: %dish_name%"
    calories_key = "Калории: %calories% ккал"
    
    meal_params = {"dish_name": "Борщ"}
    calories_params = {"calories": 350}
    
    await send_localized_message(123, meal_result_key, meal_params, russian_user["language_code"])
    await send_localized_message(456, meal_result_key, meal_params, english_user["language_code"])
    
    await send_localized_message(123, calories_key, calories_params, russian_user["language_code"])
    await send_localized_message(456, calories_key, calories_params, english_user["language_code"])
    
    # Example 4: Unsupported language (will use default language)
    spanish_user = {"language_code": "es"}
    await send_localized_message(789, message_key, user_locale=spanish_user["language_code"])

if __name__ == "__main__":
    asyncio.run(main())