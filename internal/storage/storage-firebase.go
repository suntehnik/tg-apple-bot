package storage

import (
	"errors"
	"tg-bot-food/internal/app_config"
	"tg-bot-food/internal/dto"
	"tg-bot-food/internal/firebase"
)

type Storage interface {
	CreateProfile(profile *dto.Profile) error
	GetProfile(userId string) (*dto.Profile, error)
	UpdateProfile(profile *dto.Profile) error
	DeleteProfile(userId string) error
	CreateRecord(record *dto.Record) error
	GetRecords(userId string) ([]dto.Record, error)
	UpdateRecord(record *dto.Record) error
	DeleteRecord(recordId string) error
	UploadPicture(pictureUrl string) (string, error)
}

type StorageFirebase struct {
	Firebase firebase.Firebase
}

func NewStorage(config app_config.AppConfig, app firebase.Firebase) Storage {
	return &StorageFirebase{Firebase: app}
}

func (s *StorageFirebase) CreateProfile(profile *dto.Profile) error {
	return errors.New("not implemented")
}

func (s *StorageFirebase) GetProfile(userId string) (*dto.Profile, error) {
	return nil, errors.New("not implemented")
}

func (s *StorageFirebase) UpdateProfile(profile *dto.Profile) error {
	return errors.New("not implemented")
}

func (s *StorageFirebase) DeleteProfile(userId string) error {
	return errors.New("not implemented")
}

func (s *StorageFirebase) CreateRecord(record *dto.Record) error {
	return errors.New("not implemented")
}

func (s *StorageFirebase) GetRecords(userId string) ([]dto.Record, error) {
	return nil, errors.New("not implemented")
}

func (s *StorageFirebase) UpdateRecord(record *dto.Record) error {
	return errors.New("not implemented")
}

func (s *StorageFirebase) DeleteRecord(recordId string) error {
	return errors.New("not implemented")
}

func (s *StorageFirebase) UploadPicture(pictureUrl string) (string, error) {
	return "", errors.New("not implemented")
}
