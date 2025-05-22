from typing import Dict, Any
import os
from loguru import logger


class FoodAnalysisService:
    """Service for analyzing food images."""
    
    def __init__(self, openai_service, pubsub_publisher=None):
        """
        Initialize the food analysis service.
        
        Args:
            openai_service: Service for interacting with OpenAI
            pubsub_publisher: Optional service for publishing messages to Pub/Sub
        """
        self.openai_service = openai_service
        self.pubsub_publisher = pubsub_publisher
        self.use_mock = os.environ.get("USE_MOCK_OPENAI", "false").lower() == "true"
        logger.info(f"Food analysis service initialized with mock mode: {self.use_mock}")
    
    async def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze a food image.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        logger.info(f"Analyzing food image: {image_path}")
        
        # Check if file exists
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return {
                "success": False,
                "error": "Image file not found"
            }
        
        # Check if we should use Pub/Sub for asynchronous processing
        if self.pubsub_publisher:
            # Publish to Pub/Sub and return a pending status
            message_id = await self.pubsub_publisher.publish_food_image(image_path)
            
            logger.info(f"Published food image analysis task to Pub/Sub: {message_id}")
            
            return {
                "success": True,
                "pending": True,
                "message_id": message_id
            }
        else:
            # Process synchronously
            if self.use_mock:
                # Use mock analysis for testing
                result = self.openai_service.mock_analyze_food_image(image_path)
                logger.info(f"Used mock analysis for: {image_path}")
            else:
                # Use real OpenAI Vision API
                result = await self.openai_service.analyze_food_image(image_path)
            
            # Log result summary
            if result.get("success", False):
                logger.info(f"Food image analysis successful: {result.get('food_name', 'Unknown')}")
            else:
                logger.error(f"Food image analysis failed: {result.get('error', 'Unknown error')}")
            
            return result