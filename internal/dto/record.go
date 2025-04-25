package dto

import (
	"time"
)

type Record struct {
	ID            string    `json:"id"`
	UserId        string    `json:"user_id"`
	DateTime      time.Time `json:"date_time"`
	Calories      int       `json:"calories"`
	Protein       int       `json:"protein"`
	Fat           int       `json:"fat"`
	Carbohydrates int       `json:"carbohydrates"`
	PictureUrl    string    `json:"picture_url"`
}
