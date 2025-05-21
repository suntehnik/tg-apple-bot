package registration

import "fmt"

type RegistrationMemoryStorage struct {
	storage map[uint64]*UserSession
}

type RegistrationStorage interface {
	GetSession(userId uint64) (*UserSession, error)
	CreateSession(userId uint64) error
	UpdateSession(userId uint64, session *UserSession) error
	DeleteSession(userId uint64) error
}

func NewRegistrationMemoryStorage() RegistrationStorage {
	return &RegistrationMemoryStorage{
		storage: make(map[uint64]*UserSession),
	}
}

func (s *RegistrationMemoryStorage) GetSession(userId uint64) (*UserSession, error) {
	if session, ok := s.storage[userId]; ok {
		return session, nil
	}
	return nil, fmt.Errorf("session not found")
}

func (s *RegistrationMemoryStorage) CreateSession(userId uint64) error {
	s.storage[userId] = &UserSession{
		UserId:          userId,
		CurrentScenario: "registration",
	}
	return nil
}

func (s *RegistrationMemoryStorage) UpdateSession(userId uint64, session *UserSession) error {
	s.storage[userId] = session
	return nil
}

func (s *RegistrationMemoryStorage) DeleteSession(userId uint64) error {
	delete(s.storage, userId)
	return nil
}
