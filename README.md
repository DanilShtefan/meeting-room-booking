# Сервис бронирования переговорных комнат

API для бронирования переговорок в коворкинге с JWT-аутентификацией, ролями (user/admin) и PostgreSQL.

## Стек

Python 3.11+, FastAPI, SQLAlchemy (async), PostgreSQL, Alembic, Docker

## Локальный запуск

```bash
# 1. PostgreSQL должен быть запущен на localhost:5432, БД meeting_room_booking
# 2. Установить зависимости
cd backend && poetry install
# 3. Применить миграции
poetry run alembic upgrade head
# 4. Заполнить тестовыми данными
poetry run python seed.py
# 5. Запустить
poetry run uvicorn app.main:app --reload
```

### Переменные окружения (опционально)

| Переменная | По умолчанию | Описание |
|---|---|---|
| DB_HOST | localhost | Хост PostgreSQL |
| DB_PORT | 5432 | Порт PostgreSQL |
| DB_USER | postgres | Пользователь |
| DB_PASS | postgres | Пароль |
| DB_NAME | meeting_room_booking | Имя БД |
| JWT_SECRET | secret-key-change-me | Секрет для JWT |

## Docker

```bash
docker compose up --build
```

Бэкенд на `http://localhost:8000`, документация Swagger: `http://localhost:8000/docs`

## Тестовые пользователи

| Логин | Пароль | Роль |
|-------|--------|------|
| admin | admin | Администратор |
| user  | user  | Сотрудник |

## API Endpoints

| Метод | Путь | Описание | Auth |
|-------|------|----------|------|
| POST | /api/v1/auth/login | Получить JWT токен | — |
| GET | /api/v1/rooms/ | Список комнат со слотами | — |
| GET | /api/v1/rooms/{id}/availability?date= | Занятые слоты на дату | — |
| POST | /api/v1/bookings/ | Создать бронь | + |
| DELETE | /api/v1/bookings/{id} | Отменить бронь (свою или любую для admin) | + |
| GET | /api/v1/bookings/my | Мои бронирования | + |

### Примеры

**Логин:**

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"login": "user", "password": "user"}'
```

Ответ:
```json
{"access_token": "eyJ...", "token_type": "bearer"}
```

**Список комнат:**

```bash
curl http://localhost:8000/api/v1/rooms/
```

**Создать бронь:**

```bash
curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"room_id": 1, "slot_id": 2, "date": "2026-07-10"}'
```

**Мои брони:**

```bash
curl http://localhost:8000/api/v1/bookings/my \
  -H "Authorization: Bearer <token>"
```

**Отменить бронь:**

```bash
curl -X DELETE http://localhost:8000/api/v1/bookings/1 \
  -H "Authorization: Bearer <token>"
```

## Тесты

```bash
cd backend && poetry run pytest -v
```

Перед тестами нужно запустить PostgreSQL на порту 5434 с БД meeting_room_booking_test (или настроить в tests/conftest.py).

## Фронтенд

```bash
cd frontend && npm install && npm run dev
```

Доступен на `http://localhost:5173`, проксирует /api на бэкенд.
