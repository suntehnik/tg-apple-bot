from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MealDTO(BaseModel):
    """Data Transfer Object for meal information."""
    
    id: Optional[str] = None
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    meal_type: str = "snack"  # breakfast, lunch, dinner, snack
    food_name: str
    calories: float
    proteins: float
    fats: float
    carbs: float
    image_url: Optional[str] = None
    
    def to_dict(self):
        """Convert the DTO to a dictionary for Firestore."""
        return {
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "meal_type": self.meal_type,
            "food_name": self.food_name,
            "calories": self.calories,
            "proteins": self.proteins,
            "fats": self.fats,
            "carbs": self.carbs,
            "image_url": self.image_url
        }
    
    @classmethod
    def from_dict(cls, id: str, data: dict):
        """Create a DTO from a Firestore document."""
        return cls(
            id=id,
            user_id=data.get("user_id"),
            timestamp=data.get("timestamp"),
            meal_type=data.get("meal_type", "snack"),
            food_name=data.get("food_name"),
            calories=data.get("calories"),
            proteins=data.get("proteins"),
            fats=data.get("fats"),
            carbs=data.get("carbs"),
            image_url=data.get("image_url")
        )