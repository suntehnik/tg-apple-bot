"""
Simplified interface for localization service.
This module provides a more convenient way to access the localization service.
"""
from typing import Dict, Any, Optional
from pathlib import Path
import os

from core.localization.localization_service import LocalizationService

# Default locales directory is relative to this file
DEFAULT_LOCALES_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / "locale"

# Get the singleton instance
_localization_service = LocalizationService()

def init(locales_dir: str = None, default_language: str = "ru"):
    """
    Initialize the localization service.
    
    Args:
        locales_dir: Directory containing locale files (default: core/localization/locale)
        default_language: Default language code (default: ru)
    """
    directory = locales_dir or str(DEFAULT_LOCALES_DIR)
    _localization_service.load_locales(directory, default_language)

def gettext(key: str, user_locale: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> str:
    """
    Get a localized string based on user's Telegram locale.
    
    Args:
        key: Original string in Russian
        user_locale: User's Telegram locale code (if None, default language is used)
        params: Dictionary with values for placeholders in format %key%
        
    Returns:
        Localized string
    """
    # Map Telegram locale to our supported language
    language = map_telegram_locale(user_locale) if user_locale else None
    return _localization_service.get(key, language, params)

def map_telegram_locale(telegram_locale: str) -> str:
    """
    Map Telegram locale code to our supported language code.
    
    Args:
        telegram_locale: Telegram locale code (e.g., 'en', 'ru', 'es-ES', etc.)
        
    Returns:
        Mapped language code that we support
    """
    # Extract base language from locale (e.g., 'en-US' -> 'en')
    base_locale = telegram_locale.split('-')[0].lower() if telegram_locale else None
    
    # If we have an exact match in our available languages, use it
    if base_locale and base_locale in _localization_service.available_languages:
        return base_locale
        
    # Otherwise return None and let the service use the default language
    return None

def get_available_languages() -> list:
    """Get a list of available languages."""
    return _localization_service.available_languages

def get_default_language() -> str:
    """Get the default language."""
    return _localization_service.default_language