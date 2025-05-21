package registration

import (
	"errors"
	"fmt"
	"strconv"
	"tg-bot-food/internal/scenarios"
)

const (
	NameStep          = "name"
	AgeStep           = "age"
	GenderStep        = "gender"
	WeightStep        = "weight"
	TargetWeightStep  = "target_weight"
	HeightStep        = "height"
	ActivityLevelStep = "activity_level"
)

type RegistrationSession struct {
	Target      *RegistrationScenarioTarget
	CurrentStep ScenarioStep
}

type RegistrationScenario struct {
	Items   map[ScenarioStep]StepItem
	Session *RegistrationSession
}

func NewRegistrationScenario() scenarios.Scenario {
	return &RegistrationScenario{
		Session: &RegistrationSession{
			Target:      &RegistrationScenarioTarget{},
			CurrentStep: NameStep,
		},
		Items: map[ScenarioStep]StepItem{
			NameStep:          {Question: "Как вас зовут?", NextStep: AgeStep},
			AgeStep:           {Question: "Сколько вам лет?", NextStep: GenderStep},
			GenderStep:        {Question: "Какой у вас пол?", NextStep: WeightStep},
			WeightStep:        {Question: "Сколько кг вы весите?", NextStep: TargetWeightStep},
			TargetWeightStep:  {Question: "Сколько кг вы хотите весить?", NextStep: HeightStep},
			HeightStep:        {Question: "Сколько см вы в росте?", NextStep: ActivityLevelStep},
			ActivityLevelStep: {Question: "Каков ваш уровень активности?"},
		},
	}
}

func (s *RegistrationScenario) HandleMessage(userId int64, message string, photoUrl string) (string, error) {
	session, err := restoreSessionOrNew(userId)
	if err != nil {
		s.Session = &RegistrationSession{
			Target:      &RegistrationScenarioTarget{},
			CurrentStep: NameStep,
		}
		saveSession(userId, s.Session)
		return s.Items[s.Session.CurrentStep].Question, nil
	}
	switch session.CurrentStep {
	case NameStep:
		{
			Name, err := validateName(message)
			if err != nil {
				return "Вы ввели недопустимое имя", fmt.Errorf("invalid name: %v", err)
			}
			s.Session.Target.Name = Name
			s.Session.CurrentStep = AgeStep
		}
	case AgeStep:
		{
			age, err := strconv.Atoi(message)
			if err != nil {
				return "Вы ввели недопустимый возраст", fmt.Errorf("invalid age: %v", err)
			}
			s.Session.Target.Age = age
			s.Session.CurrentStep = GenderStep
		}
	case GenderStep:
		{
			gender := message
			s.Session.Target.Gender = gender
			s.Session.CurrentStep = WeightStep
		}
	case WeightStep:
		{
			weight, err := strconv.Atoi(message)
			if err != nil {
				return "Вы ввели недопустимый вес", fmt.Errorf("invalid weight: %v", err)
			}
			s.Session.Target.Weight = weight
			s.Session.CurrentStep = TargetWeightStep
		}
	case TargetWeightStep:
		{
			targetWeight, err := strconv.Atoi(message)
			if err != nil {
				return "Вы ввели недопустимый целевой вес", fmt.Errorf("invalid target weight: %v", err)
			}
			s.Session.Target.TargetWeight = targetWeight
			s.Session.CurrentStep = HeightStep
		}
	case HeightStep:
		{
			height, err := strconv.Atoi(message)
			if err != nil {
				return "Вы ввели недопустимый рост", fmt.Errorf("invalid height: %v", err)
			}
			s.Session.Target.Height = height
			s.Session.CurrentStep = ActivityLevelStep
		}
	case ActivityLevelStep:
		{
			activityLevel := message
			s.Session.Target.ActivityLevel = activityLevel
			s.Session.CurrentStep = DoneStep
			saveSession(userId, s.Session)
			return "Спасибо! Ваш профиль создан.", nil
		}
	case DoneStep:
		{
			return "Спасибо! Ваш профиль создан.", nil
		}
	}
	saveSession(userId, s.Session)
	return s.Items[s.Session.CurrentStep].Question, nil
}

var userSessions = make(map[int64]*RegistrationSession)

func restoreSessionOrNew(userId int64) (*RegistrationSession, error) {
	if session, ok := userSessions[userId]; ok {
		return session, nil
	} else {
		return nil, fmt.Errorf("session not found")
	}
}

func saveSession(userId int64, session *RegistrationSession) {
	userSessions[userId] = session
}

func validateName(name string) (string, error) {
	if name == "" {
		return "", errors.New("name cannot be empty")
	}
	return name, nil
}
