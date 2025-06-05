import pytest
from unittest.mock import MagicMock
from config.config import Config
from core.services.telegram import TelegramService
from core.services.firestore import FirestoreService
from core.services.openai import OpenAIService
from services.user_service import UserService
from services.meal_service import MealService
from services.food_analysis import FoodAnalysisService
from scenarios.orchestrator import ScenarioOrchestrator


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    config = Config(
        telegram_token="mock_token",
        openai_api_key="mock_key",
        firestore_credentials_path="mock_path",
        log_level="INFO"
    )
    return config


@pytest.fixture
def mock_telegram_service(mock_config):
    """Create a mock Telegram service."""
    service = MagicMock(spec=TelegramService)
    service.config = mock_config
    return service


@pytest.fixture
def mock_firestore_service(mock_config):
    """Create a mock Firestore service."""
    service = MagicMock(spec=FirestoreService)
    service.config = mock_config
    return service


@pytest.fixture
def mock_openai_service(mock_config):
    """Create a mock OpenAI service."""
    service = MagicMock(spec=OpenAIService)
    service.config = mock_config
    return service


@pytest.fixture
def mock_user_service(mock_firestore_service):
    """Create a mock user service."""
    service = MagicMock(spec=UserService)
    service.firestore_service = mock_firestore_service
    return service


@pytest.fixture
def mock_meal_service(mock_firestore_service):
    """Create a mock meal service."""
    service = MagicMock(spec=MealService)
    service.firestore_service = mock_firestore_service
    return service


@pytest.fixture
def mock_food_analysis_service(mock_openai_service):
    """Create a mock food analysis service."""
    service = MagicMock(spec=FoodAnalysisService)
    service.openai_service = mock_openai_service
    return service


@pytest.fixture
def mock_orchestrator():
    """Create a mock scenario orchestrator."""
    orchestrator = MagicMock(spec=ScenarioOrchestrator)
    orchestrator.scenarios = {}
    orchestrator.active_scenarios = {}
    return orchestrator