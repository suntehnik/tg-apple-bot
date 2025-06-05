#!/usr/bin/env python3
"""
Script to test the OpenAI Vision API with food images.
This can be run directly to test the OpenAI integration.
"""

import os
import sys
import json
import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("openai-test")

# Try to load API key from environment
api_key = os.environ.get("OPENAI_API_KEY")

# Define a simple Config class
class Config:
    def __init__(self, **kwargs):
        self.telegram_token = kwargs.get("telegram_token", "test_token")
        self.openai_api_key = kwargs.get("openai_api_key", api_key)
        self.firestore_credentials_path = kwargs.get("firestore_credentials_path", "test_path")
        self.log_level = kwargs.get("log_level", "INFO")


# Define a simplified OpenAIService class
class OpenAIService:
    def __init__(self, config):
        self.config = config
        self.api_key = config.openai_api_key
        if self.api_key:
            logger.info(f"OpenAI service initialized with key: {self.api_key[:4]}...")
        else:
            logger.info("No API key provided")
        
        # OpenAI package is not used in this simple test
        self.openai = None
    
    async def analyze_food_image(self, image_path):
        """
        Analyze a food image using OpenAI Vision API.
        In this demo, we'll just use mock responses.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Analysis results
        """
        logger.info(f"Analyzing image: {image_path}")
        
        # Check if image exists
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return {
                "success": False,
                "error": "Image file not found"
            }
        
        # Return mock responses based on the image name
        image_name = os.path.basename(image_path).lower()
        
        if "pizza" in image_name:
            mock_response = {
                "success": True,
                "food_name": "Pizza",
                "calories": 285,
                "proteins": 12,
                "fats": 10,
                "carbs": 36
            }
        elif "salad" in image_name:
            mock_response = {
                "success": True,
                "food_name": "Garden Salad",
                "calories": 150,
                "proteins": 3,
                "fats": 10,
                "carbs": 12
            }
        elif "burger" in image_name:
            mock_response = {
                "success": True,
                "food_name": "Hamburger",
                "calories": 550,
                "proteins": 25,
                "fats": 30,
                "carbs": 45
            }
        else:
            mock_response = {
                "success": True,
                "food_name": "Unknown Food",
                "calories": 300,
                "proteins": 15,
                "fats": 12,
                "carbs": 30
            }
        
        logger.info(f"Using mock response for {image_name}: {mock_response['food_name']}")
        return mock_response


async def main():
    """Main function to run the OpenAI Vision API test."""
    config = Config()
    openai_service = OpenAIService(config)
    
    # Paths to test images
    test_images = {
        'pizza': os.path.join('tests', 'img', 'pizza.jpg'),
        'salad': os.path.join('tests', 'img', 'salad.jpg'),
        'burger': os.path.join('tests', 'img', 'burger.jpg'),
    }
    
    print("\n=== OpenAI Vision API Test ===\n")
    
    for food_type, image_path in test_images.items():
        print(f"\n--- Testing {food_type.upper()} image ---")
        
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"⚠️  Test image {image_path} does not exist")
            continue
        
        # Analyze the image
        result = await openai_service.analyze_food_image(image_path)
        
        # Print the result
        print(f"Result for {food_type}:")
        print(json.dumps(result, indent=2))
        
        # Print nutritional info in a nice format
        if result["success"]:
            print(f"\n📊 Nutritional Information for {result['food_name']}:")
            print(f"🔥 Calories: {result['calories']} kcal")
            print(f"🥩 Protein:  {result['proteins']} g")
            print(f"🧈 Fat:      {result['fats']} g")
            print(f"🍚 Carbs:    {result['carbs']} g")
    
    print("\n=== Test Completed ===\n")
    print("Note: This test used mock responses. To use real OpenAI API,")
    print("set the OPENAI_API_KEY environment variable and modify the script to use the OpenAI package.")


if __name__ == "__main__":
    try:
        # For Python 3.7+
        asyncio.run(main())
    except AttributeError:
        # For older Python versions
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())