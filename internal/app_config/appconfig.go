package app_config

import "os"

type AppConfig struct {
	FirebaseCredentialsFilePath string
	TelegramBotToken            string
}

func NewAppConfig() AppConfig {
	return AppConfig{
		FirebaseCredentialsFilePath: os.Getenv("GOOGLE_APPLICATION_CREDENTIALS"),
		TelegramBotToken:            os.Getenv("TELEGRAM_BOT_TOKEN"),
	}
}
