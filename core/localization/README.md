# Localization Module

This module provides localization support for the Telegram bot, allowing messages to be translated based on the user's locale.

## Features

- Support for multiple languages (currently Russian and English)
- Automatic detection of user's language from Telegram locale
- String placeholder replacement with `%key%` format
- Fallback to primary language (Russian) when translation is not available
- Singleton service implementation for easy access throughout the codebase

## Usage

### Initialization

Initialize the localization service at application startup:

```python
from core.localization import init

# Initialize with default settings
init()

# Or specify a custom locale directory and default language
init(locales_dir="/path/to/locales", default_language="ru")
```

### Getting Localized Strings

Use the `get` function to retrieve localized strings:

```python
from core.localization import get

# Basic usage - returns the string in the default language
message = get("Привет! Я бот для отслеживания питания.")

# With user's Telegram locale
user_locale = message.from_user.language_code
message = get("Привет! Я бот для отслеживания питания.", user_locale)

# With placeholder replacement
name = "John"
message = get("Спасибо, %name%! Какой у вас рост (в см)?", user_locale, {"name": name})
```

### Usage with Telegram Service

Integrate with the Telegram service for sending localized messages:

```python
async def send_message(self, chat_id: int, key: str, params=None, parse_mode=ParseMode.HTML):
    # Get user locale from user data (implementation depends on your user management)
    user = await self.get_user(chat_id)
    user_locale = user.get("language_code") if user else None
    
    # Get localized message
    localized_text = get(key, user_locale, params)
    
    # Send message
    await self.bot.send_message(chat_id=chat_id, text=localized_text, parse_mode=parse_mode)
```

## Adding New Languages

To add a new language:

1. Create a new JSON file in the `locale/` directory named after the language code (e.g., `fr.json` for French)
2. Copy the structure of `ru.json` and translate the values to the new language
3. Keep the keys unchanged (they are the original Russian strings)

## File Structure

- `locale/ru.json` - Primary language strings (Russian)
- `locale/en.json` - English translations
- `localization_service.py` - Core implementation of the localization service
- `i18n.py` - Simplified interface for accessing the localization service
- `__init__.py` - Module exports