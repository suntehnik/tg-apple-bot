package main

import (
	"log"
	"tg-bot-food/internal/app_config"
	"tg-bot-food/internal/bot"
	"tg-bot-food/internal/firebase"
)

func main() {
	appConfig := app_config.NewAppConfig()
	_, err := firebase.InitFirebase(appConfig)
	if err != nil {
		log.Fatal(err)
	}
	bot.StartBot(appConfig)
}
