package openai

import (
	context "context"

	"github.com/sashabaranov/go-openai"
)

// ChatGPTClient определяет интерфейс для клиента ChatGPT
// Позволяет легко мокать и подменять реализацию в тестах
type ChatGPTClient interface {
	SendMessageWithImage(ctx context.Context, message, imageURL string) (*openai.ChatCompletionResponse, error)
}

type Client struct {
	api *openai.Client
}

func NewClient(apiKey string) ChatGPTClient {
	return &Client{api: openai.NewClient(apiKey)}
}

// Client реализует ChatGPTClient
func (c *Client) SendMessageWithImage(ctx context.Context, message, imageURL string) (*openai.ChatCompletionResponse, error) {

	chatMessagePromptContent := openai.ChatMessagePart{
		Type: openai.ChatMessagePartTypeText,
		Text: message,
	}
	chatMessageImageContent := openai.ChatMessagePart{
		Type: openai.ChatMessagePartTypeImageURL,
		ImageURL: &openai.ChatMessageImageURL{
			URL: imageURL,
		},
	}
	msg := openai.ChatCompletionMessage{
		Role: openai.ChatMessageRoleUser,
		MultiContent: []openai.ChatMessagePart{
			chatMessagePromptContent,
			chatMessageImageContent,
		},
	}

	// Используем CreateChatCompletion с передачей raw messages
	resp, err := c.api.CreateChatCompletion(ctx, openai.ChatCompletionRequest{
		Model:    openai.GPT4Turbo,
		Messages: []openai.ChatCompletionMessage{msg},
	})
	return &resp, err
}
