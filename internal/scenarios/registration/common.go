package registration

type ScenarioStep string

const (
	DoneStep = "done"
)

type StepItem struct {
	Question string
	NextStep ScenarioStep
}

type RegistrationScenarioTarget struct {
	Name          string
	Age           int
	Gender        string
	Weight        int
	TargetWeight  int
	Height        int
	ActivityLevel string
}

type UserSession struct {
	UserId          uint64
	CurrentScenario string
	CurrentStep     ScenarioStep
	Target          *RegistrationScenarioTarget
}
