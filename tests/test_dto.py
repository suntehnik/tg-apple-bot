from datetime import datetime
from dto.profile import UserProfileDTO
from dto.meal import MealDTO


def test_user_profile_dto():
    """Test the UserProfileDTO class."""
    # Create a user profile
    profile = UserProfileDTO(
        telegram_id=123456789,
        username="testuser",
        first_name="Test",
        last_name="User",
        goals={"weight": 70, "calories": 2000}
    )
    
    # Check that fields are set correctly
    assert profile.telegram_id == 123456789
    assert profile.username == "testuser"
    assert profile.first_name == "Test"
    assert profile.last_name == "User"
    assert profile.goals == {"weight": 70, "calories": 2000}
    assert profile.id is None
    assert isinstance(profile.registration_date, datetime)
    
    # Test to_dict method
    profile_dict = profile.to_dict()
    assert profile_dict["telegram_id"] == 123456789
    assert profile_dict["username"] == "testuser"
    assert profile_dict["first_name"] == "Test"
    assert profile_dict["last_name"] == "User"
    assert profile_dict["goals"] == {"weight": 70, "calories": 2000}
    assert "id" not in profile_dict
    assert isinstance(profile_dict["registration_date"], datetime)
    
    # Test from_dict method
    reconstructed = UserProfileDTO.from_dict("user123", profile_dict)
    assert reconstructed.id == "user123"
    assert reconstructed.telegram_id == profile.telegram_id
    assert reconstructed.username == profile.username
    assert reconstructed.first_name == profile.first_name
    assert reconstructed.last_name == profile.last_name
    assert reconstructed.goals == profile.goals


def test_meal_dto():
    """Test the MealDTO class."""
    # Create a meal
    meal = MealDTO(
        user_id="user123",
        food_name="Pizza",
        calories=800.5,
        proteins=20.3,
        fats=30.1,
        carbs=90.7,
        meal_type="dinner"
    )
    
    # Check that fields are set correctly
    assert meal.user_id == "user123"
    assert meal.food_name == "Pizza"
    assert meal.calories == 800.5
    assert meal.proteins == 20.3
    assert meal.fats == 30.1
    assert meal.carbs == 90.7
    assert meal.meal_type == "dinner"
    assert meal.id is None
    assert meal.image_url is None
    assert isinstance(meal.timestamp, datetime)
    
    # Test to_dict method
    meal_dict = meal.to_dict()
    assert meal_dict["user_id"] == "user123"
    assert meal_dict["food_name"] == "Pizza"
    assert meal_dict["calories"] == 800.5
    assert meal_dict["proteins"] == 20.3
    assert meal_dict["fats"] == 30.1
    assert meal_dict["carbs"] == 90.7
    assert meal_dict["meal_type"] == "dinner"
    assert "id" not in meal_dict
    assert meal_dict["image_url"] is None
    assert isinstance(meal_dict["timestamp"], datetime)
    
    # Test from_dict method
    reconstructed = MealDTO.from_dict("meal456", meal_dict)
    assert reconstructed.id == "meal456"
    assert reconstructed.user_id == meal.user_id
    assert reconstructed.food_name == meal.food_name
    assert reconstructed.calories == meal.calories
    assert reconstructed.proteins == meal.proteins
    assert reconstructed.fats == meal.fats
    assert reconstructed.carbs == meal.carbs
    assert reconstructed.meal_type == meal.meal_type
    assert reconstructed.image_url == meal.image_url