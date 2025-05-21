package scenarios

type Scenario interface {
	HandleMessage(userId int64, message string, photoUrl string) (string, error)
}

type ScenarioOrchestrator interface {
	HandleMessage(userId int64, message string, photoUrl string) (string, error)
}

type TgScenarioOrchestrator struct {
	RegistrationScenario Scenario
	UpdateMealScenario   Scenario
	activeScenario       Scenario
}

func NewTgScenarioOrchestrator(registrationScenario Scenario, updateMealScenario Scenario) ScenarioOrchestrator {
	return &TgScenarioOrchestrator{
		RegistrationScenario: registrationScenario,
		UpdateMealScenario:   updateMealScenario,
		activeScenario:       updateMealScenario,
	}
}

func (s *TgScenarioOrchestrator) HandleMessage(userId int64, message string, photoUrl string) (string, error) {
	return s.activeScenario.HandleMessage(userId, message, photoUrl)
}
