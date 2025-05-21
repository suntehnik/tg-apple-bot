package updatemeal

import (
	"fmt"
	"log"
	"tg-bot-food/internal/scenarios"
	"time"
)

type TelegramUpdateMealScenario struct {
	MealStorage  MealStorage
	VisionClient VisionClient // абстракция Vision API
}

type VisionClient interface {
	SendImage(imageURL string) (string, error)
}

func NewTelegramUpdateMealScenario(mealStorage MealStorage, visionClient VisionClient) scenarios.Scenario {
	return &TelegramUpdateMealScenario{
		MealStorage:  mealStorage,
		VisionClient: visionClient,
	}
}

func (s *TelegramUpdateMealScenario) HandleMessage(userId int64, message string, photoUrl string) (string, error) {
	meal := &Meal{
		Name:          "",
		ImageUrl:      photoUrl,
		DateTime:      time.Now().Format("2006-01-02 15:04:05"),
		Comment:       message,
		Calories:      0,
		Proteins:      0,
		Fats:          0,
		Carbohydrates: 0,
	}

	resp := "Ваша заявка принята, спасибо за звонок"
	var err error
	// Если есть VisionClient, отправляем изображение и промпт в ChatGPT Vision
	if photoUrl != "" {
		resp, err = s.VisionClient.SendImage(photoUrl)
		if err != nil {
			return "", err
		}
		meal.Name = resp
	}

	err = s.MealStorage.CreateMeal(userId, meal)
	if err != nil {
		log.Println(err)
		return fmt.Sprintf("Произошла ошибка при создании заявки: %s", err.Error()), err
	}

	return resp, nil
}
