import os
import json
from dotenv import load_dotenv
from .config import Config


class ConfigManager:
    """Manages loading configuration from environment variables or a file."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._config = None
        return cls._instance
    
    def load_config(self, env_file_path=None, config_file_path=None):
        """
        Load configuration from environment variables or a file.
        
        Args:
            env_file_path (str, optional): Path to .env file
            config_file_path (str, optional): Path to config.json file
            
        Returns:
            Config: The loaded configuration
        """
        # Load environment variables from .env file if provided
        if env_file_path and os.path.exists(env_file_path):
            load_dotenv(env_file_path)
        
        # If config file is provided and exists, load from it
        if config_file_path and os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config_dict = json.load(f)
            self._config = Config(**config_dict)
        else:
            # Load from environment variables
            self._config = Config(
                telegram_token=os.getenv("TELEGRAM_TOKEN"),
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                firestore_credentials_path=os.getenv("FIRESTORE_CREDENTIALS_PATH"),
                pubsub_project_id=os.getenv("PUBSUB_PROJECT_ID"),
                pubsub_topic=os.getenv("PUBSUB_TOPIC"),
                pubsub_subscription=os.getenv("PUBSUB_SUBSCRIPTION"),
                log_level=os.getenv("LOG_LEVEL", "INFO")
            )
        
        return self._config
    
    @property
    def config(self):
        """
        Get the current configuration.
        
        Returns:
            Config: The current configuration
        """
        if self._config is None:
            self.load_config()
        return self._config