package updatemeal

type Meal struct {
	Name          string `json:"name"`
	Calories      int    `json:"calories"`
	Proteins      int    `json:"proteins"`
	Fats          int    `json:"fats"`
	Carbohydrates int    `json:"carbohydrates"`
	ImageUrl      string `json:"image_url"`
	DateTime      string `json:"date_time"`
	Comment       string `json:"comment"`
}
