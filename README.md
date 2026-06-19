# telegram-task-bot

Простой Telegram-бот для управления задачами с использованием aiogram, PostgreSQL (Neon) и SQLAlchemy async.

## Возможности

- Добавление задач через кнопки
- Просмотр списка задач
- Отметка задач как выполненных
- Удаление задач
- Хранение данных в PostgreSQL (Neon)
- Асинхронная работа (aiogram 3 + async SQLAlchemy)

## Технологии

- Python 3.11+
- aiogram 3.x
- SQLAlchemy 2.x (async)
- asyncpg
- PostgreSQL (Neon)
- Railway (деплой)

## Установка

```bash
git clone https://github.com/your-username/telegram-task-bot.git
cd telegram-task-bot
pip install -r requirements.txt
```

## Интерфейс бота (кнопки)

Бот управляется через кнопочное меню (без команд).

Основные кнопки:
- Добавить задачу
- Список задач
- Выполнить задачу
- Удалить задачу

## Переменные окружения

Создайте файл .env или добавьте переменные в Railway:

BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname?sslmode=require

## Запуск локально

```bash
python boot.py
```

## Структура проекта

app/
 ├── boot.py
 ├── handlers.py
 ├── service.py
 ├── database.py
 ├── models.py

## Деплой (Railway)

1. Подключить GitHub репозиторий
2. Добавить переменные окружения (BOT_TOKEN, DATABASE_URL)
3. Railway автоматически задеплоит проект

## Возможные проблемы

### TelegramConflictError
Запущено два экземпляра бота.
Решение: оставить только один запуск (локально или Railway).

## Автор

Тамаев Альберт Георгиевич

Учебный проект для практики:

- Telegram Bot API
- Async Python
- PostgreSQL
