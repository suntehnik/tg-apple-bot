// internal/bot/bot.go
package bot

import (
	"log"

	app_config "tg-bot-food/internal/app_config"
	"tg-bot-food/internal/scenarios"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func StartBot(appConfig app_config.AppConfig, scenarioOrchestrator scenarios.ScenarioOrchestrator) {
	botToken := appConfig.TelegramBotToken
	if botToken == "" {
		log.Fatal("TELEGRAM_BOT_TOKEN environment variable is not set")
	}

	bot, err := tgbotapi.NewBotAPI(botToken)
	if err != nil {
		log.Panic(err)
	}

	log.Printf("Authorized on account %s", bot.Self.UserName)

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60

	updates := bot.GetUpdatesChan(u)

	for update := range updates {
		if update.Message == nil {
			continue
		}
		photoUrl := ""
		if update.Message.Photo != nil {
			fileID := update.Message.Photo[0].FileID
			photoUrl, err = bot.GetFileDirectURL(fileID)
			if err != nil {
				log.Printf("Error getting file: %v", err)
				continue
			}
		}
		msg, err := scenarioOrchestrator.HandleMessage(update.Message.From.ID, update.Message.Text, photoUrl)
		if err != nil {
			log.Printf("Error handling message: %v", err)
			continue
		}
		tgMsg := tgbotapi.NewMessage(update.Message.Chat.ID, msg)
		bot.Send(tgMsg)
	}
}
