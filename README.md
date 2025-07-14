# ITK-test-task

Wallet Management API with FastAPI, PostgreSQL, and Docker

## Описание

REST API для управления кошельками с поддержкой операций пополнения и снятия средств. Приложение построено с использованием FastAPI, PostgreSQL и Docker.

## Технологический стек

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (async)
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest
- **Documentation**: OpenAPI/Swagger
- **Logging**: Structured logging with trace IDs

## Архитектура

```
src/
├── application/           # Business logic layer
│   ├── services/         # Service implementations
│   ├── contracts/        # Service interfaces
│   └── exceptions/       # Custom exceptions
├── infrastructure/       # Infrastructure layer
│   ├── database/         # Database models & repositories
│   ├── logger/           # Logging configuration
│   └── middleware/       # HTTP middleware
└── presentation/         # Presentation layer
    ├── routing/          # API routes
    └── schemas/          # Pydantic models
```

## API Endpoints

### Создание кошелька
```http
POST /wallets/create
```

### Получение баланса
```http
GET /wallets/{wallet_id}
```

### Операции с кошельком
```http
POST /wallets/{wallet_id}/operation
```

**Параметры:**
- `amount`: Сумма операции (float)
- `operation_type`: Тип операции ("DEPOSIT" или "WITHDRAW")

## Установка и запуск

### Предварительные требования
- Docker
- Docker Compose

### Запуск приложения

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Noloquideus/ITK-test-task
cd itk-test-task
```

2. Заполните файл `.env`(Заранее заполнен):

```bash
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DOCS_USERNAME=admin
DOCS_PASSWORD=admin123
```

3. Запустите приложение:
```bash
docker-compose up --build
```

4. Приложение будет доступно по адресу:
- API: http://localhost:9000
- Документация: http://localhost:9000/docs

## Тестирование

### Структура тестов
```
tests/
├── conftest.py              # Pytest configuration
├── unit/                    # Unit tests
│   ├── test_wallet_service.py
│   └── test_wallet_repository.py
└── integration/             # Integration tests
    └── test_wallet_api.py
```

### Запуск тестов

1. Установите зависимости для тестов:
```bash
pip install -r requirements-test.txt
```

2. Запустите тесты:
```bash
# Все тесты
pytest

# Только unit тесты
pytest tests/unit/

# Только integration тесты
pytest tests/integration/

# С покрытием кода
pytest --cov=src --cov-report=html
```

### Покрытие тестами
- ✅ Unit тесты для сервисов
- ✅ Unit тесты для репозиториев
- ✅ Integration тесты для API
- ✅ Тестирование ошибок и edge cases
- ✅ Mocking внешних зависимостей

## Особенности реализации

### Конкурентность
- Использование row-level locking для предотвращения race conditions
- Транзакционная обработка операций
- Правильная обработка ошибок с rollback

### Точность вычислений
- Использование `Decimal` вместо `float` для денежных операций
- Точность до 2 знаков после запятой
- Предотвращение ошибок округления

### Безопасность
- Валидация входных данных
- Проверка достаточности средств
- Логирование всех операций
- Обработка исключений

### Масштабируемость
- Асинхронная архитектура
- Dependency injection
- Четкое разделение слоев
- Легко тестируемый код


# Таска
```
Добрый день, уважаемый соискатель, данное задание нацелено на выявление вашего реального уровня в разработке на python, поэтому отнеситесь к нему, как к работе на проекте. Выполняйте его честно и проявите себя по максимуму, удачи! 
Напишите приложение, которое по REST принимает запрос вида
POST api/v1/wallets/<WALLET_UUID>/operation
{
operation_type: “DEPOSIT” or “WITHDRAW”,
amount: 1000
}
после выполнять логику по изменению счета в базе данных
также есть возможность получить баланс кошелька
GET api/v1/wallets/{WALLET_UUID}
стек:
FastAPI / Flask / Django
Postgresql

Код должен следовать PEP8.
Должны быть написаны миграции для базы данных.
Обратите особое внимание проблемам при работе в конкурентной среде, параллельные запросы на изменения баланса одного кошелька должны работать корректно.
Приложение должно запускаться в докер контейнере, база данных тоже, вся система должна подниматься с помощью docker-compose
Эндпоинты должны быть покрыты тестами.
Решенное задание залить на гитхаб, предоставить ссылку
Все возникающие вопросы по заданию решать самостоятельно, по своему усмотрению.
```
