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

---

## М3

### Промпт

Задание М3: Dockerfile для Rust-приложения.

Создай CLI-утилиту `textutil` на Rust (только std, без внешних зависимостей).
Команды: count, reverse, upper, lower — результат в JSON.
Двухстадийный Dockerfile: builder на `rust:1.75`, финальный на `debian:bookworm-slim`.
Не менее 20 unit-тестов через `#[cfg(test)]`.

### Результат

Создана структура `rust/`:
- `rust/src/main.rs` — CLI-утилита с командами count/reverse/upper/lower, вывод JSON, обработка ошибок (exit code 1 + JSON с "error")
- `rust/Cargo.toml` — пакет textutil, edition 2021, без зависимостей
- `rust/Dockerfile` — двухстадийная сборка с кэшированием зависимостей через заглушку
- `rust/.dockerignore`
- 27 unit-тестов: count (слова/символы/строки/пустая строка), reverse (обычная/палиндром/один символ/пустая), upper/lower (смешанный регистр), граничные случаи (нет аргументов, неизвестная команда, команда без текста)
