# Архитектура проекта "Чат-бот для отслеживания питания и диеты"

## Общая структура проекта

```
tg-bot-food/
├── app.py                   # Основная точка входа приложения
├── Dockerfile               # Инструкции для сборки Docker-образа
├── requirements.txt         # Зависимости проекта
├── config/                  # Конфигурационные файлы
│   ├── config_manager.py    # Загрузчик конфигурации
│   └── config.py            # DTO для конфигурации
├── core/                    # Ядро приложения
│   ├── services/             # Сервисы для внешних сервисов
│   │   ├── telegram.py      # Сервис для Telegram API (aiogram)
│   │   ├── firestore.py     # Сервис для Google Firestore
│   │   └── openai.py        # Сервис для OpenAI API
│   ├── logging/             # Модуль логирования
│   │   └── logger.py        # Настройка и управление логированием
│   └── pubsub/              # Модуль для работы с Google Cloud Pub/Sub
│       ├── publisher.py     # Публикация сообщений
│       └── subscriber.py    # Подписка на сообщения
├── dto/                     # Data Transfer Objects
│   ├── profile.py           # DTO профиля пользователя
│   └── meal.py              # DTO информации о приеме пищи
├── scenarios/               # Сценарии взаимодействия с пользователем
│   ├── base.py              # Базовый абстрактный класс сценария
│   ├── registration/        # Сценарий регистрации
│   │   └── registration.py  # Реализация сценария регистрации
│   └── meal/                # Сценарий добавления приема пищи
│       └── meal_photo.py    # Реализация сценария добавления фото еды
└── services/                # Бизнес-логика
    ├── food_analysis.py     # Сервис анализа фотографий еды
    ├── user_service.py      # Сервис управления пользователями
    └── meal_service.py      # Сервис управления приемами пищи
```

## Модули и их назначение

### 1. Конфигурация (config/)
- **config_manager.py**: Загружает конфигурацию из файла, переменных окружения.
- **config.py**: DTO для хранения параметров конфигурации.

### 2. Сервисы (core/services/)
- **telegram.py**: Сервис для взаимодействия с Telegram API через aiogram.
- **firestore.py**: Сервис для работы с базой данных Google Firestore.
- **openai.py**: Сервис для взаимодействия с OpenAI API (Computer Vision).

### 3. Логирование (core/logging/)
- **logger.py**: Настройка логирования, обработка и форматирование логов.

### 4. Pub/Sub (core/pubsub/)
- **publisher.py**: Публикация сообщений в Google Cloud Pub/Sub.
- **subscriber.py**: Подписка на сообщения из Google Cloud Pub/Sub.

### 5. DTO (dto/)
- **profile.py**: DTO для хранения информации о пользователе.
- **meal.py**: DTO для хранения информации о приеме пищи.

### 6. Сценарии (scenarios/)
- **base.py**: Абстрактный класс сценария.
- **registration/registration.py**: Реализация сценария регистрации пользователя.
- **meal/meal_photo.py**: Реализация сценария добавления фото еды.

### 7. Сервисы (services/)
- **food_analysis.py**: Сервис для анализа фотографий еды с использованием OpenAI.
- **user_service.py**: Сервис для управления пользователями.
- **meal_service.py**: Сервис для управления приемами пищи.

## Ключевые классы и их контракты

### Config
```python
class Config:
    telegram_token: str
    openai_api_key: str
    firestore_credentials_path: str
    pubsub_project_id: str
    pubsub_topic: str
    pubsub_subscription: str
    log_level: str
```

### TelegramService
```python
class TelegramService:
    def __init__(self, config: Config, scenario_orchestrator):
        # Инициализация с конфигурацией и оркестратором сценариев
        
    async def start_polling(self):
        # Запуск бота в режиме поллинга
        
    async def send_message(self, chat_id: int, text: str):
        # Отправка текстового сообщения
        
    async def send_photo(self, chat_id: int, photo_path: str, caption: str = None):
        # Отправка фотографии
    async def HandleMessage(self, message: Message):
        # Обработка сообщения от пользователя c фотографией и текстом
```

### FirestoreService
```python
class FirestoreService:
    def __init__(self, config: Config):
        # Инициализация с конфигурацией
        
    def save_user(self, user_profile: UserProfileDTO):
        # Сохранение профиля пользователя
        
    def get_user(self, user_id: str) -> UserProfileDTO:
        # Получение профиля пользователя
        
    def save_meal(self, meal: MealDTO):
        # Сохранение информации о приеме пищи
        
    def get_meals(self, user_id: str, from_date=None, to_date=None) -> List[MealDTO]:
        # Получение информации о приемах пищи
```

### OpenAIService
```python
class OpenAIService:
    def __init__(self, config: Config):
        # Инициализация с конфигурацией
        
    async def analyze_food_image(self, image_path: str) -> dict:
        # Анализ изображения еды с помощью OpenAI Vision
        # Возвращает словарь с информацией о блюде, калориях, БЖУ
```

### AbstractScenario
```python
class AbstractScenario(ABC):
    @abstractmethod
    async def start(self, context: dict) -> dict:
        # Запуск сценария
        pass
    
    @abstractmethod
    async def next_step(self, context: dict, input_data: dict) -> dict:
        # Переход к следующему шагу сценария
        pass
    
    @abstractmethod
    async def cancel(self, context: dict) -> dict:
        # Отмена сценария
        pass
```

### RegistrationScenario
```python
class RegistrationScenario(AbstractScenario):
    def __init__(self, user_service):
        # Инициализация с сервисом пользователей
        
    async def start(self, context: dict) -> dict:
        # Начало процесса регистрации
        
    async def next_step(self, context: dict, input_data: dict) -> dict:
        # Обработка данных от пользователя на текущем шаге
        
    async def cancel(self, context: dict) -> dict:
        # Отмена регистрации
```

### MealPhotoScenario
```python
class MealPhotoScenario(AbstractScenario):
    def __init__(self, food_analysis_service, meal_service):
        # Инициализация с сервисами
        
    async def start(self, context: dict) -> dict:
        # Начало процесса добавления фото еды
        
    async def next_step(self, context: dict, input_data: dict) -> dict:
        # Обработка фото от пользователя
        
    async def cancel(self, context: dict) -> dict:
        # Отмена добавления
```

### UserProfileDTO
```python
class UserProfileDTO:
    id: str
    telegram_id: int
    username: str
    first_name: str
    last_name: str
    registration_date: datetime
    goals: dict  # Цели по питанию, активности и т.д.
```

### MealDTO
```python
class MealDTO:
    id: str
    user_id: str
    timestamp: datetime
    meal_type: str  # Например: breakfast, lunch, dinner, snack
    food_name: str
    calories: float
    proteins: float
    fats: float
    carbs: float
    image_url: str  # Опционально, URL изображения в хранилище
```

### ScenarioOrchestrator
```python
class ScenarioOrchestrator:
    def __init__(self, scenarios: dict):
        # Инициализация с словарем сценариев
        
    async def start_scenario(self, scenario_name: str, user_id: int, context: dict = None) -> dict:
        # Запуск сценария для пользователя
        
    async def process_update(self, user_id: int, update_data: dict) -> dict:
        # Обработка обновления от пользователя и передача в активный сценарий
```

### FoodAnalysisService
```python
class FoodAnalysisService:
    def __init__(self, openai_facade, pubsub_publisher):
        # Инициализация с фасадом OpenAI и издателем Pub/Sub
        
    async def analyze_image(self, image_path: str) -> dict:
        # Анализ изображения еды
        # Публикация задачи в Pub/Sub (если необходимо)
        # Возврат результатов анализа
```

### UserService
```python
class UserService:
    def __init__(self, firestore_facade):
        # Инициализация с фасадом Firestore
        
    def create_user(self, telegram_user_data: dict) -> UserProfileDTO:
        # Создание нового пользователя
        
    def get_user(self, user_id: str) -> UserProfileDTO:
        # Получение пользователя
        
    def update_user(self, user_profile: UserProfileDTO) -> UserProfileDTO:
        # Обновление данных пользователя
```

### MealService
```python
class MealService:
    def __init__(self, firestore_facade):
        # Инициализация с фасадом Firestore
        
    def add_meal(self, user_id: str, meal_data: dict) -> MealDTO:
        # Добавление записи о приеме пищи
        
    def get_user_meals(self, user_id: str, from_date=None, to_date=None) -> List[MealDTO]:
        # Получение записей о приемах пищи
        
    def get_user_stats(self, user_id: str, from_date=None, to_date=None) -> dict:
        # Получение статистики по приемам пищи
```

## Поток данных

1. **Регистрация пользователя:**
   - Пользователь начинает диалог с ботом
   - Активируется сценарий регистрации
   - Данные пользователя сохраняются в Firestore через фасад

2. **Отправка фото еды:**
   - Пользователь отправляет фотографию еды
   - Активируется сценарий добавления фото еды
   - Фото отправляется на анализ через OpenAI Vision
   - Результаты анализа возвращаются пользователю
   - Данные сохраняются в Firestore

3. **Получение статистики:**
   - Пользователь запрашивает статистику
   - Данные извлекаются из Firestore
   - Статистика отображается пользователю

## Расширение функциональности

1. Модульная структура позволяет легко добавлять новые сценарии
2. Фасадный паттерн обеспечивает абстракцию от конкретных реализаций API
3. Использование DTO упрощает передачу данных между компонентами
