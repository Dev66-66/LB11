# Prompt Log

## М1

### Промпт

Задание М1: Dockerfile для Python-приложения (из ЛР №6).

Изучи репозиторий ЛР №6: https://github.com/Dev66-66/LB6
Flask-приложение со слоёной архитектурой (routes/, services/, repositories/).
Основной модуль — sqlite.py с Blueprint item_routes: CRUD для предметов через SQLite.

Создай в текущей папке структуру `python/` со всеми необходимыми файлами:
- `python/app.py` — точка входа (sqlite.py) + эндпоинт GET /health
- `python/routes/item_routes.py` — Blueprint с CRUD API
- `python/services/item_service.py` — сервисный слой
- `python/repositories/item_repository.py` — слой репозитория (SQLite)
- `python/requirements.txt` — зависимости
- `python/Dockerfile` — двухстадийная сборка (builder + python:3.12-slim)
- `python/tests/test_items.py` — 20+ pytest тестов
- `python/.dockerignore`

### Результат

Создана структура `python/` на основе ЛР №6:
- Скопированы и адаптированы файлы `routes/item_routes.py`, `services/item_service.py`, `repositories/item_repository.py`
- В `repositories/item_repository.py` добавлен метод `_init_db()` для автоматического создания таблицы
- В `routes/item_routes.py` добавлена обработка пустого тела запроса (None JSON → 400)
- В `app.py` добавлен эндпоинт `GET /health → {"status": "ok"}`
- Написано 27 тестов: CRUD, 404, структура JSON, HTTP статус-коды, граничные случаи
- Двухстадийный Dockerfile: builder на `python:3.12`, финальный образ на `python:3.12-slim`
- Все тесты проходят (`pytest python/tests/ -v`)
