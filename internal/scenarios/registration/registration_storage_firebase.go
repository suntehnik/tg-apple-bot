package registration

import (
	"context"
	"strconv"
	"tg-bot-food/internal/firebase"

	"cloud.google.com/go/firestore"
)

type RegistrationFirebaseStorage struct {
	Firebase firebase.Firebase
}

func (s *RegistrationFirebaseStorage) CreateSession(userId uint64) error {
	ctx := context.Background()
	firestoreClient, err := s.Firebase.App.Firestore(ctx)
	if err != nil {
		return err
	}
	defer firestoreClient.Close()
	newSession := &UserSession{
		UserId:          userId,
		CurrentScenario: "registration",
		CurrentStep:     "",
		Target:          nil,
	}
	_, err = firestoreClient.Collection("users").Doc(strconv.FormatUint(userId, 10)).Set(ctx, newSession, firestore.MergeAll)
	return err
}

func (s *RegistrationFirebaseStorage) GetSession(userId uint64) (*UserSession, error) {
	ctx := context.Background()
	firestoreClient, err := s.Firebase.App.Firestore(ctx)
	if err != nil {
		return nil, err
	}
	defer firestoreClient.Close()
	userDoc, err := firestoreClient.Collection("users").Doc(strconv.FormatUint(userId, 10)).Get(ctx)
	if err != nil {
		return nil, err
	}
	if !userDoc.Exists() {
		return nil, nil
	}
	var session UserSession
	err = userDoc.DataTo(&session)
	if err != nil {
		return nil, err
	}
	return &session, nil
}

func (s *RegistrationFirebaseStorage) UpdateSession(userId uint64, session *UserSession) error {
	ctx := context.Background()
	firestoreClient, err := s.Firebase.App.Firestore(ctx)
	if err != nil {
		return err
	}
	defer firestoreClient.Close()
	_, err = firestoreClient.Collection("users").Doc(strconv.FormatUint(userId, 10)).Set(ctx, session, firestore.MergeAll)
	return err
}

func (s *RegistrationFirebaseStorage) DeleteSession(userId uint64) error {
	ctx := context.Background()
	firestoreClient, err := s.Firebase.App.Firestore(ctx)
	if err != nil {
		return err
	}
	defer firestoreClient.Close()
	_, err = firestoreClient.Collection("users").Doc(strconv.FormatUint(userId, 10)).Delete(ctx)
	return err
}

func NewRegistrationFirebaseStorage(firebase firebase.Firebase) RegistrationStorage {
	return &RegistrationFirebaseStorage{
		Firebase: firebase,
	}
}
