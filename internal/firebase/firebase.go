package firebase

import (
	"context"
	"log"

	firebase "firebase.google.com/go/v4"
	"google.golang.org/api/option"

	app_config "tg-bot-food/internal/app_config"
)

type Firebase struct {
	App *firebase.App
}

// InitFirebase инициализирует Firebase App с использованием serviceAccountKey.json или переменных окружения
func InitFirebase(config app_config.AppConfig) (Firebase, error) {
	ctx := context.Background()
	keyPath := config.FirebaseCredentialsFilePath
	if keyPath == "" {
		log.Fatal("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")
	}
	opt := option.WithCredentialsFile(keyPath)
	app, err := firebase.NewApp(ctx, nil, opt)
	if err != nil {
		log.Fatalf("error initializing firebase app: %v", err)
	}
	return Firebase{App: app}, nil
}
