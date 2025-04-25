package firebase

import (
	"context"
	"log"
	"os"

	"firebase.google.com/go/v4"
	"google.golang.org/api/option"
)

// App содержит экземпляр Firebase App
var App *firebase.App

// InitFirebase инициализирует Firebase App с использованием serviceAccountKey.json или переменных окружения
func InitFirebase() {
	ctx := context.Background()
	keyPath := os.Getenv("GOOGLE_APPLICATION_CREDENTIALS")
	if keyPath == "" {
		log.Fatal("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")
	}
	opt := option.WithCredentialsFile(keyPath)
	app, err := firebase.NewApp(ctx, nil, opt)
	if err != nil {
		log.Fatalf("error initializing firebase app: %v", err)
	}
	App = app
}
