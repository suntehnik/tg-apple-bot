from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration model for the application."""
    
    # Telegram Bot configuration
    telegram_token: str = Field(..., description="Telegram Bot API token")
    
    # OpenAI configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    
    # Firebase configuration
    firestore_credentials_path: str = Field(..., description="Path to Firebase credentials file")
    
    # PubSub configuration (optional)
    pubsub_project_id: str = Field(None, description="Google Cloud project ID for Pub/Sub")
    pubsub_topic: str = Field(None, description="Pub/Sub topic for food analysis")
    pubsub_subscription: str = Field(None, description="Pub/Sub subscription for food analysis")
    
    # Logging configuration
    log_level: str = Field("INFO", description="Logging level")