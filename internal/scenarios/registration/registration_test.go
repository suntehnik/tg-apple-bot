package registration

import (
	"testing"
)

func TestRegistrationScenario(t *testing.T) {
	// Проверка создания нового сценария
	s := NewRegistrationScenario()
	if s == nil {
		t.Fatal("NewRegistrationScenario() вернул nil")
	}
}

func TestRegistrationScenario_HandleMessage(t *testing.T) {
	// Проверка прохождения всех этапов регистрации
	s := NewRegistrationScenario()
	userId := int64(1)

	steps := []struct {
		input      string
		inputImage string
		expected   string
	}{
		{"", "", "Как вас зовут?"},
		{"Иван", "", "Сколько вам лет?"},
		{"25", "", "Какой у вас пол?"},
		{"мужской", "", "Сколько кг вы весите?"},
		{"80", "", "Сколько кг вы хотите весить?"},
		{"75", "", "Сколько см вы в росте?"},
		{"180", "", "Каков ваш уровень активности?"},
		{"высокий", "", "Спасибо! Ваш профиль создан."},
	}

	for i, step := range steps {
		msg, _ := s.HandleMessage(userId, step.input, step.inputImage)
		if msg != step.expected {
			t.Errorf("Шаг %d: ожидалось '%s', получено '%s'", i, step.expected, msg)
		}
	}
}
