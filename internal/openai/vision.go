package openai

import (
	"context"

	app_config "tg-bot-food/internal/app_config"
)

// VisionClient — абстракция для работы с Vision API (OpenAI)
type VisionClient interface {
	SendImage(imageURL string) (string, error)
}

// visionAdapter реализует VisionClient через ChatGPTClient
// Возвращает string-ответ для пользователя
// Можно расширять/менять логику преобразования

type visionAdapter struct {
	client ChatGPTClient
	prompt string
}

func NewVisionClient(appConfig app_config.AppConfig, client ChatGPTClient) VisionClient {
	return &visionAdapter{client: client, prompt: appConfig.OpenAIPrompt}
}

func (v *visionAdapter) SendImage(imageURL string) (string, error) {
	ctx := context.Background()
	resp, err := v.client.SendMessageWithImage(ctx, v.prompt, imageURL)
	if err != nil {
		return "", err
	}
	if resp == nil || len(resp.Choices) == 0 {
		return "OpenAI не вернул ответ", nil
	}
	return resp.Choices[0].Message.Content, nil
}
