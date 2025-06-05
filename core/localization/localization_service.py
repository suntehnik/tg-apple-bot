import json
import os
import re
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class LocalizationService:
    """
    Service for handling localization of strings in the application.
    Implemented as a singleton.
    """
    _instance = None
    _placeholder_pattern = re.compile(r'%(\w+)%')
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocalizationService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the localization service with default values."""
        self._strings = {}
        self._default_language = "ru"  # Russian is the primary language
        self._loaded = False
    
    def load_locales(self, locale_dir: str, default_language: str = "ru"):
        """
        Load all locale files from the specified directory.
        
        Args:
            locale_dir: Directory containing locale JSON files
            default_language: Default language to use (default: ru)
        """
        self._default_language = default_language
        locale_path = Path(locale_dir)
        
        if not locale_path.exists():
            logger.error(f"Locale directory not found: {locale_path}")
            return
            
        # Load all available locale files
        loaded_languages = []
        for locale_file in locale_path.glob("*.json"):
            language = locale_file.stem
            try:
                with open(locale_file, 'r', encoding='utf-8') as f:
                    self._strings[language] = json.load(f)
                loaded_languages.append(language)
            except Exception as e:
                logger.error(f"Failed to load locale file {locale_file}: {e}")
        
        if loaded_languages:
            logger.info(f"Loaded localization for languages: {', '.join(loaded_languages)}")
            self._loaded = True
        else:
            logger.warning("No localization files were loaded")
    
    def get(self, key: str, language: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Get a localized string for the given key and language.
        
        Args:
            key: The string in the primary language (Russian) to be localized
            language: Target language code (if None, default language is used)
            params: Dictionary with values for placeholders in format %key%
            
        Returns:
            Localized string or the original key if not found
        """
        if not self._loaded:
            logger.warning("Localization service not loaded. Using original string.")
            return self._replace_placeholders(key, params or {})
            
        language = language or self._default_language
        
        # If language not available, return the original key
        if language not in self._strings:
            return self._replace_placeholders(key, params or {})
            
        # If language is available, find the translation
        translations = self._strings[language]
        if key in translations:
            return self._replace_placeholders(translations[key], params or {})
        
        # Fall back to the original key if translation not found
        return self._replace_placeholders(key, params or {})
    
    def _replace_placeholders(self, text: str, params: Dict[str, Any]) -> str:
        """
        Replace all placeholders in format %key% with corresponding values from params.
        
        Args:
            text: Text containing placeholders
            params: Dictionary with values for placeholders
            
        Returns:
            Text with replaced placeholders
        """
        if not params:
            return text
            
        def _replace_match(match):
            key = match.group(1)
            return str(params.get(key, match.group(0)))
            
        return self._placeholder_pattern.sub(_replace_match, text)
    
    @property
    def available_languages(self) -> list:
        """Get a list of available languages."""
        return list(self._strings.keys())
    
    @property
    def default_language(self) -> str:
        """Get the default language."""
        return self._default_language