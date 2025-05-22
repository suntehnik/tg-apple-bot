import os
import pytest
import tempfile
import json
from config.config_manager import ConfigManager
from config.config import Config


def test_config_model():
    """Test the Config model."""
    # Create a config object with required fields
    config = Config(
        telegram_token="test_token",
        openai_api_key="test_key",
        firestore_credentials_path="test_path"
    )
    
    # Check that fields are set correctly
    assert config.telegram_token == "test_token"
    assert config.openai_api_key == "test_key"
    assert config.firestore_credentials_path == "test_path"
    assert config.log_level == "INFO"  # Default value
    assert config.pubsub_project_id is None  # Optional field


def test_config_manager_env_vars():
    """Test loading configuration from environment variables."""
    # Set environment variables
    os.environ["TELEGRAM_TOKEN"] = "env_token"
    os.environ["OPENAI_API_KEY"] = "env_key"
    os.environ["FIRESTORE_CREDENTIALS_PATH"] = "env_path"
    os.environ["LOG_LEVEL"] = "DEBUG"
    
    # Create config manager and load config
    manager = ConfigManager()
    config = manager.load_config()
    
    # Check that fields are set correctly from environment variables
    assert config.telegram_token == "env_token"
    assert config.openai_api_key == "env_key"
    assert config.firestore_credentials_path == "env_path"
    assert config.log_level == "DEBUG"
    
    # Clean up
    del os.environ["TELEGRAM_TOKEN"]
    del os.environ["OPENAI_API_KEY"]
    del os.environ["FIRESTORE_CREDENTIALS_PATH"]
    del os.environ["LOG_LEVEL"]


def test_config_manager_file():
    """Test loading configuration from a file."""
    # Create a temporary config file
    config_data = {
        "telegram_token": "file_token",
        "openai_api_key": "file_key",
        "firestore_credentials_path": "file_path",
        "log_level": "ERROR"
    }
    
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
        json.dump(config_data, temp)
        temp_path = temp.name
    
    try:
        # Create config manager and load config from file
        manager = ConfigManager()
        config = manager.load_config(config_file_path=temp_path)
        
        # Check that fields are set correctly from file
        assert config.telegram_token == "file_token"
        assert config.openai_api_key == "file_key"
        assert config.firestore_credentials_path == "file_path"
        assert config.log_level == "ERROR"
    finally:
        # Clean up
        os.unlink(temp_path)