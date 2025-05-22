import os
from typing import Dict, Any
import openai
from loguru import logger
from config.config import Config


class OpenAIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self, config: Config):
        """
        Initialize the OpenAI service.
        
        Args:
            config (Config): Application configuration
        """
        self.config = config
        self.client = openai.AsyncOpenAI(api_key=config.openai_api_key)
        logger.info("OpenAI service initialized")
        
    
    async def analyze_food_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze a food image using OpenAI Vision API.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict[str, Any]: Analysis results including food name, calories, protein, fat, carbs
        """
        logger.info(f"Analyzing food image: {image_path}")
        
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return {
                    "success": False,
                    "error": "Image file not found"
                }
            
            # Read image file
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                # Convert to base64 if needed
                import base64
                image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Create a vision prompt
            prompt = """
            Analyze this food image and identify:
            1. The name of the dish or food item
            2. Approximate calories
            3. Protein content (in grams)
            4. Fat content (in grams)
            5. Carbohydrate content (in grams)
            
            Return the information in a structured format like this:
            {
                "food_name": "name of the dish",
                "calories": number,
                "proteins": number,
                "fats": number,
                "carbs": number
            }
            
            Only return the JSON object, nothing else.
            """
            
            # Call the OpenAI API
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=500,
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            # Process the response to extract JSON
            import json
            import re
            
            # Find JSON pattern in response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                result = json.loads(json_str)
                
                # Add success flag
                result["success"] = True
                
                logger.info(f"Food analysis successful: {result['food_name']}")
                return result
            else:
                logger.error("Failed to parse JSON from OpenAI response")
                return {
                    "success": False,
                    "error": "Failed to parse analysis results",
                    "raw_response": content
                }
                
        except Exception as e:
            logger.error(f"Error analyzing food image: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def mock_analyze_food_image(self, image_path: str) -> Dict[str, Any]:
        """
        Mock analysis of a food image for testing without API calls.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict[str, Any]: Mock analysis results
        """
        # Determine food type from filename
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