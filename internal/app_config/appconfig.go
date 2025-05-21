package app_config

import "os"

type AppConfig struct {
	FirebaseCredentialsFilePath string
	FirebaseProjectId           string
	TelegramBotToken            string
	OpenAIApiKey                string
	OpenAIPrompt                string
}

func NewAppConfig() AppConfig {
	return AppConfig{
		FirebaseCredentialsFilePath: os.Getenv("GOOGLE_APPLICATION_CREDENTIALS"),
		FirebaseProjectId:           os.Getenv("GOOGLE_CLOUD_PROJECT_ID"),
		TelegramBotToken:            os.Getenv("TELEGRAM_BOT_TOKEN"),
		OpenAIApiKey:                os.Getenv("OPENAI_API_KEY"),
		OpenAIPrompt:                os.Getenv("OPENAI_PROMPT"),
	}
}
