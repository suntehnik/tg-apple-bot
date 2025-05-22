import asyncio
import logging
import os
from loguru import logger

# Set up basic logging for aiogram
logging.basicConfig(level=logging.INFO)

# Import configuration
from config.config_manager import ConfigManager
from config.config import Config

# Sample function to test the setup
async def test_setup():
    logger.info("Testing application setup...")
    
    # Create a sample config
    config = Config(
        telegram_token="sample_token",
        openai_api_key="sample_key",
        firestore_credentials_path="sample_path",
        log_level="INFO"
    )
    
    logger.info(f"Created sample config: {config}")
    logger.info("Application setup test completed!")
    
    return True

if __name__ == "__main__":
    # Run the test setup
    result = asyncio.run(test_setup())
    logger.info(f"Test result: {result}")
    
    # Show success message
    logger.info("""
    =================================================
    ✅ Project structure has been created successfully!
    
    Next steps:
    1. Configure your .env file with real credentials
    2. Add Firebase credentials in the secrets directory
    3. Run the bot with 'python app.py'
    =================================================
    """)