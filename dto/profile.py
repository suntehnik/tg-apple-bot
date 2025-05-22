from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class UserProfileDTO(BaseModel):
    """Data Transfer Object for user profile information."""
    
    id: Optional[str] = None
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    registration_date: datetime = Field(default_factory=datetime.now)
    goals: Dict[str, Any] = Field(default_factory=dict)
    
    def to_dict(self):
        """Convert the DTO to a dictionary for Firestore."""
        return {
            "telegram_id": self.telegram_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "registration_date": self.registration_date,
            "goals": self.goals
        }
    
    @classmethod
    def from_dict(cls, id: str, data: dict):
        """Create a DTO from a Firestore document."""
        return cls(
            id=id,
            telegram_id=data.get("telegram_id"),
            username=data.get("username"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            registration_date=data.get("registration_date"),
            goals=data.get("goals", {})
        )