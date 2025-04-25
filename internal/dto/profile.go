package dto

type Profile struct {
	ID            string `json:"id"`
	UserId        string `json:"user_id"`
	Name          string `json:"name"`
	Age           int    `json:"age"`
	Gender        string `json:"gender"`
	Weight        int    `json:"weight"`
	Height        int    `json:"height"`
	ActivityLevel string `json:"activity_level"`
	Goal          string `json:"goal"`
}
