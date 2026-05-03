# 🚀 PersonalHub

![Python](https://img.shields.io/badge/python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-enabled-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Backend-приложение для управления задачами в формате Kanban (boards / columns / tasks).

---

## ✨ Возможности

- 📌 Boards (доски)
- 📊 Columns (колонки)
- ✅ Tasks (задачи)
- 🔗 Связи: Board → Columns → Tasks
- 🧠 Enum-типизация (workspace, column type, urgency)
- ⚡ Полностью async (FastAPI + SQLAlchemy 2.0)

---

## 🏗️ Архитектура

```
src/
├── app/            # приложение (lifespan, логгеры)
├── database/       # postgres + alembic
├── entities/       # ORM модели + enums
├── interfaces/     # API (routes, validation, dependencies)
├── logic/          # бизнес-логика
├── settings/       # конфигурация
└── main.py         # точка входа
```

---

## ⚙️ Стек

- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Alembic
- structlog
- Docker
- uv (package manager)
- pytest + testcontainers

---

## 🚀 Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/Dimylkin/personalhub.git
cd personalhub
```

---

### 2. Настройка env

```bash
cp .env.example .env
```

---

### 3. Запуск

```bash
docker compose up --build
```

---

### 4. Swagger

```
http://localhost:8000/api/docs
```

---

## 🗄️ Миграции

### Создать миграцию

```bash
docker compose exec app alembic revision --autogenerate -m "message"
```

### Применить

```bash
docker compose exec app alembic upgrade head
```

⚠️ Миграции автоматически применяются при старте приложения

---

## 🧪 Тесты

Тесты полностью изолированы (используется testcontainers).

```bash
uv run pytest -v
```

❗ Docker должен быть запущен

---

## 📊 Логирование

- structlog (JSON)
- Разделение dev / prod
- SQL логирование (опционально)

---

## 📦 API

### Boards

| Метод | URL | Описание |
|------|-----|--------|
| GET | `/api/boards` | список |
| GET | `/api/boards/{id}` | получить |
| POST | `/api/boards` | создать |
| PATCH | `/api/boards/{id}` | обновить |
| DELETE | `/api/boards/{id}` | удалить |

---

## 🧱 Пример запроса

```json
POST /api/boards

{
  "workspace": "work"
}
```

---

## 👨‍💻 Разработка

### Локальный запуск (без Docker)

```bash
uv sync
uv run python src/main.py
```

---

## 📄 Лицензия

MIT