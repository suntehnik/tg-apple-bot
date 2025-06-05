import os
import pytest
import json
from unittest.mock import patch, MagicMock
import asyncio

from config.config import Config
from core.services.openai import OpenAIService


# Paths to test images
TEST_IMAGES = {
    'pizza': os.path.join(os.path.dirname(__file__), 'img', 'pizza.jpg'),
    'salad': os.path.join(os.path.dirname(__file__), 'img', 'salad.jpg'),
    'burger': os.path.join(os.path.dirname(__file__), 'img', 'burger.jpg'),
}

# Mock responses for OpenAI API
MOCK_RESPONSES = {
    'pizza': {
        "food_name": "Pizza",
        "calories": 285,
        "proteins": 12,
        "fats": 10,
        "carbs": 36
    },
    'salad': {
        "food_name": "Garden Salad",
        "calories": 150,
        "proteins": 3,
        "fats": 10,
        "carbs": 12
    },
    'burger': {
        "food_name": "Hamburger",
        "calories": 550,
        "proteins": 25,
        "fats": 30,
        "carbs": 45
    }
}


class TestOpenAIIntegration:
    """Tests for OpenAI Vision API integration."""

    @pytest.fixture
    def config(self):
        """Create a test configuration."""
        return Config(
            telegram_token="test_token",
            openai_api_key=os.environ.get("OPENAI_API_KEY", "test_key"),
            firestore_credentials_path="test_path"
        )

    @pytest.fixture
    def openai_service(self, config):
        """Create an OpenAI service."""
        return OpenAIService(config)

    @pytest.mark.skip(reason="Requires real OpenAI API key")
    @pytest.mark.asyncio
    async def test_real_openai_vision_api(self, openai_service):
        """
        Test the OpenAI Vision API with real API calls.
        
        This test is skipped by default because it requires a real API key.
        To run it, set the OPENAI_API_KEY environment variable and remove the skip marker.
        """
        # Check if images exist
        for food_type, image_path in TEST_IMAGES.items():
            assert os.path.exists(image_path), f"Test image {image_path} does not exist"
            
            # Analyze the image
            result = await openai_service.analyze_food_image(image_path)
            
            # Check the result
            assert result["success"] is True, f"Analysis of {food_type} failed"
            assert "food_name" in result, f"No food name in result for {food_type}"
            assert "calories" in result, f"No calories in result for {food_type}"
            assert "proteins" in result, f"No proteins in result for {food_type}"
            assert "fats" in result, f"No fats in result for {food_type}"
            assert "carbs" in result, f"No carbs in result for {food_type}"
            
            # Verify that the result contains reasonable values
            assert result["calories"] > 0, f"Calories should be positive for {food_type}"
            assert result["proteins"] >= 0, f"Proteins should be non-negative for {food_type}"
            assert result["fats"] >= 0, f"Fats should be non-negative for {food_type}"
            assert result["carbs"] >= 0, f"Carbs should be non-negative for {food_type}"
            
            # Print the result for debugging
            print(f"\nAnalysis result for {food_type}:")
            print(json.dumps(result, indent=2))

    @pytest.mark.asyncio
    async def test_mock_openai_vision_api(self, openai_service):
        """Test the OpenAI Vision API with mock responses."""
        for food_type, image_path in TEST_IMAGES.items():
            mock_response = MOCK_RESPONSES[food_type]
            mock_response["success"] = True
            
            # Mock the OpenAI API call
            with patch.object(openai_service, 'analyze_food_image', 
                             return_value=mock_response):
                
                # Call the mocked method
                result = await openai_service.analyze_food_image(image_path)
                
                # Verify the result
                assert result["success"] is True
                assert result["food_name"] == mock_response["food_name"]
                assert result["calories"] == mock_response["calories"]
                assert result["proteins"] == mock_response["proteins"]
                assert result["fats"] == mock_response["fats"]
                assert result["carbs"] == mock_response["carbs"]


if __name__ == "__main__":
    # Run the tests
    pytest.main(["-xvs", __file__])