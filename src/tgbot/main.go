package main

import (
	"tg-bot-food/internal/bot"
	"tg-bot-food/internal/firebase"
)

func main() {
	firebase.InitFirebase()
	bot.StartBot()
}
