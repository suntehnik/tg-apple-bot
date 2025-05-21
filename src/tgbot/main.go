package main

import (
	"log"
	"tg-bot-food/internal/app_config"
	"tg-bot-food/internal/bot"
	"tg-bot-food/internal/firebase"
	"tg-bot-food/internal/openai"
	"tg-bot-food/internal/scenarios"
	"tg-bot-food/internal/scenarios/registration"
	"tg-bot-food/internal/scenarios/updatemeal"
)

func main() {
	appConfig := app_config.NewAppConfig()
	firebase, err := firebase.InitFirebase(appConfig)
	if err != nil {
		log.Fatal(err)
	}
	registrationScenario := registration.NewRegistrationScenario()
	mealStorage, err := updatemeal.NewMealStorage(firebase)
	if err != nil {
		log.Fatal(err)
	}
	// Инициализация OpenAI Vision клиента
	visionClient := openai.NewVisionClient(appConfig, openai.NewClient(appConfig.OpenAIApiKey))
	updateMealScenario := updatemeal.NewTelegramUpdateMealScenario(mealStorage, visionClient)
	scenarioOrchestrator := scenarios.NewTgScenarioOrchestrator(registrationScenario, updateMealScenario)
	bot.StartBot(appConfig, scenarioOrchestrator)
}
