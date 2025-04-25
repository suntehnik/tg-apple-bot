# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o bot ./src/tgbot/main.go

FROM alpine:3.19
WORKDIR /app
COPY --from=builder /app/bot ./bot
COPY --from=builder /app/README.md ./README.md

# Установить переменную окружения для токена бота (можно переопределить при запуске)
ENV TELEGRAM_BOT_TOKEN=""

CMD ["./bot"]
