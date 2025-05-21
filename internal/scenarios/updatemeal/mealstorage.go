package updatemeal

import (
	"context"
	"strconv"
	"tg-bot-food/internal/firebase"
	"time"
)

type MealStorage interface {
	CreateMeal(userId int64, meal *Meal) error
	GetMeal(userId int64) (*Meal, error)
	UpdateMeal(userId int64, meal *Meal) error
	DeleteMeal(userId int64) error
}

type FirebaseMealStorage struct {
	Firebase firebase.Firebase
}

func NewMealStorage(firebase firebase.Firebase) (MealStorage, error) {
	return &FirebaseMealStorage{
		Firebase: firebase,
	}, nil
}

// implement methods
func (s *FirebaseMealStorage) CreateMeal(userId int64, meal *Meal) error {
	ctx := context.Background()
	firestoreClient := s.Firebase.Firestore
	timeStamp := time.Now().UTC().UnixMilli()
	_, err := firestoreClient.Collection("meals").
		Doc(strconv.FormatInt(userId, 10)).
		Collection("history").
		Doc(strconv.FormatInt(timeStamp, 10)).
		Set(ctx, meal)
	return err
}

func (s *FirebaseMealStorage) GetMeal(userId int64) (*Meal, error) {
	ctx := context.Background()
	firestoreClient := s.Firebase.Firestore
	mealDoc, err := firestoreClient.Collection("meals").Doc(strconv.FormatInt(userId, 10)).Get(ctx)
	if err != nil {
		return nil, err
	}
	if !mealDoc.Exists() {
		return nil, nil
	}
	var meal Meal
	err = mealDoc.DataTo(&meal)
	if err != nil {
		return nil, err
	}
	return &meal, nil
}

func (s *FirebaseMealStorage) UpdateMeal(userId int64, meal *Meal) error {
	ctx := context.Background()
	firestoreClient := s.Firebase.Firestore
	_, err := firestoreClient.Collection("meals").Doc(strconv.FormatInt(userId, 10)).Set(ctx, meal)
	return err
}

func (s *FirebaseMealStorage) DeleteMeal(userId int64) error {
	ctx := context.Background()
	firestoreClient := s.Firebase.Firestore
	_, err := firestoreClient.Collection("meals").Doc(strconv.FormatInt(userId, 10)).Delete(ctx)
	return err
}
