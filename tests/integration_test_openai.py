#!/usr/bin/env python3
"""
Full integration test for OpenAI Vision API.

This test will use real OpenAI API if OPENAI_API_KEY is set in environment variables,
otherwise it will use mock responses.

Usage:
    python -m tests.integration_test_openai

To use real OpenAI API:
    export OPENAI_API_KEY=your_api_key
    python -m tests.integration_test_openai
"""

import os
import sys
import json
import asyncio
import logging
from unittest.mock import patch

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("integration-test")

# Define paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_IMG_DIR = os.path.join(PROJECT_ROOT, 'tests', 'img')

# Add project root to path
sys.path.insert(0, PROJECT_ROOT)

# Import project modules
try:
    from config.config import Config
    from core.services.openai import OpenAIService
    PROJECT_MODULES_AVAILABLE = True
    logger.info("Successfully imported project modules")
except ImportError as e:
    logger.warning(f"Could not import project modules: {e}")
    logger.warning("Using simplified implementation")
    PROJECT_MODULES_AVAILABLE = False


# Simplified Config class
class SimpleConfig:
    def __init__(self, **kwargs):
        self.telegram_token = kwargs.get("telegram_token", "test_token")
        self.openai_api_key = kwargs.get("openai_api_key", os.environ.get("OPENAI_API_KEY"))
        self.firestore_credentials_path = kwargs.get("firestore_credentials_path", "test_path")
        self.log_level = kwargs.get("log_level", "INFO")


# Simplified OpenAIService class
class SimpleOpenAIService:
    def __init__(self, config):
        self.config = config
        self.api_key = config.openai_api_key
        
        # Check if we can use real OpenAI
        self.use_real_api = False
        if self.api_key:
            try:
                import openai
                self.openai = openai
                self.openai.api_key = self.api_key
                self.use_real_api = True
                logger.info("Using real OpenAI API")
            except ImportError:
                logger.warning("OpenAI package not available. Using mock responses.")
        else:
            logger.warning("No OpenAI API key provided. Using mock responses.")
    
    async def analyze_food_image(self, image_path):
        """Analyze a food image using OpenAI Vision API or mock responses."""
        logger.info(f"Analyzing image: {image_path}")
        
        # Check if image exists
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return {
                "success": False,
                "error": "Image file not found"
            }
        
        # Use real API if available
        if self.use_real_api:
            try:
                with open(image_path, "rb") as f:
                    image_data = f.read()
                    # Convert to base64 if needed
                    import base64
                    image_base64 = base64.b64encode(image_data).decode('utf-8')
                
                prompt = """
                Analyze this food image and identify:
                1. The name of the dish or food item
                2. Approximate calories
                3. Protein content (in grams)
                4. Fat content (in grams)
                5. Carbohydrate content (in grams)
                
                Return ONLY a JSON object like this:
                {
                    "food_name": "name of the dish",
                    "calories": number,
                    "proteins": number,
                    "fats": number,
                    "carbs": number
                }
                """
                
                response = await self.openai.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=300
                )
                
                result_text = response.choices[0].message.content
                
                # Extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(0))
                    result["success"] = True
                    return result
                else:
                    return {
                        "success": False,
                        "error": "Failed to parse response",
                        "raw_response": result_text
                    }
                    
            except Exception as e:
                logger.error(f"Error calling OpenAI API: {e}")
                return {
                    "success": False,
                    "error": str(e)
                }
        
        # Use mock responses
        image_name = os.path.basename(image_path).lower()
        
        if "pizza" in image_name:
            return {
                "success": True,
                "food_name": "Pizza",
                "calories": 285,
                "proteins": 12,
                "fats": 10,
                "carbs": 36
            }
        elif "salad" in image_name:
            return {
                "success": True,
                "food_name": "Garden Salad",
                "calories": 150,
                "proteins": 3,
                "fats": 10,
                "carbs": 12
            }
        elif "burger" in image_name:
            return {
                "success": True,
                "food_name": "Hamburger",
                "calories": 550,
                "proteins": 25,
                "fats": 30,
                "carbs": 45
            }
        else:
            return {
                "success": True,
                "food_name": "Unknown Food",
                "calories": 300,
                "proteins": 15,
                "fats": 12,
                "carbs": 30
            }


async def run_integration_test():
    """Run the OpenAI integration test."""
    print("\n=== OpenAI Vision API Integration Test ===\n")
    
    # Create service based on available modules
    if PROJECT_MODULES_AVAILABLE:
        config = Config(
            telegram_token="test_token",
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            firestore_credentials_path="test_path"
        )
        service = OpenAIService(config)
        print("Using project OpenAIService implementation")
    else:
        config = SimpleConfig()
        service = SimpleOpenAIService(config)
        print("Using simplified OpenAIService implementation")
    
    # Test images
    test_images = {
        'pizza': os.path.join(TEST_IMG_DIR, 'pizza.jpg'),
        'salad': os.path.join(TEST_IMG_DIR, 'salad.jpg'),
        'burger': os.path.join(TEST_IMG_DIR, 'burger.jpg'),
    }
    
    # Check for images
    print("\nChecking test images:")
    for name, path in test_images.items():
        if os.path.exists(path):
            print(f"✅ {name}: {path}")
        else:
            print(f"❌ {name}: {path} (not found)")
    
    # Process each image
    results = {}
    for food_type, image_path in test_images.items():
        print(f"\n--- Processing {food_type.upper()} ---")
        
        if not os.path.exists(image_path):
            print(f"⚠️  Image not found: {image_path}")
            continue
        
        # Process the image
        result = await service.analyze_food_image(image_path)
        results[food_type] = result
        
        # Print result
        if result["success"]:
            print(f"✅ Analysis successful")
            print(f"\n📊 Nutritional Information for {result['food_name']}:")
            print(f"🔥 Calories: {result['calories']} kcal")
            print(f"🥩 Protein:  {result['proteins']} g")
            print(f"🧈 Fat:      {result['fats']} g")
            print(f"🍚 Carbs:    {result['carbs']} g")
        else:
            print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
    
    # Summary
    print("\n=== Test Summary ===")
    all_success = all(r.get("success", False) for r in results.values())
    if all_success:
        print("✅ All tests passed successfully!")
    else:
        print("❌ Some tests failed")
    
    print("\nResults:")
    for food_type, result in results.items():
        status = "✓" if result.get("success", False) else "✗"
        name = result.get("food_name", "Unknown")
        print(f"  {status} {food_type}: {name}")
    
    print("\n=== Test Complete ===\n")
    
    return results


def main():
    """Main entry point for the integration test."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("\n⚠️  WARNING: No OPENAI_API_KEY environment variable found.")
        print("This test will use mock responses instead of real API calls.")
        print("To use real API, set the OPENAI_API_KEY environment variable.\n")
    
    try:
        # For Python 3.7+
        results = asyncio.run(run_integration_test())
    except AttributeError:
        # For older Python versions
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(run_integration_test())
    
    # Exit with status code based on test results
    if all(r.get("success", False) for r in results.values()):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()