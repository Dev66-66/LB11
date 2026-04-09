# Prompt Log

## М1

**Количество промптов:** 1
**Дата выполнения:** 2026-04-09

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
- Все тесты проходят (`pytest python/tests/ -v`): **27 passed**

---

## М3

**Количество промптов:** 2
**Дата выполнения:** 2026-04-09

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
- 24 unit-теста: count (слова/символы/строки/пустая строка), reverse (обычная/палиндром/один символ/пустая), upper/lower (смешанный регистр), граничные случаи (нет аргументов, неизвестная команда, команда без текста)
- Все тесты проходят (`cargo test -v`): **24 passed**

---

## Н1

**Количество промптов:** 1
**Дата выполнения:** 2026-04-09

### Промпт

Задание Н1: Go-приложение со статической компиляцией в scratch-образе.

HTTP-сервис информации о системе: GET /, /health, /info, /metrics. Только stdlib.
405 при неверном методе, 404 при несуществующем пути. PORT из env, default 8080.
Не менее 40 тестов через httptest. Dockerfile: golang:1.22 → scratch.

### Результат

Создана структура `go/`:
- `go/main.go` — HTTP-сервер с 4 эндпоинтами + вспомогательные функции `writeJSON`, `newMux`
- `go/main_test.go` — 53 теста: статус-коды, Content-Type, валидный JSON, обязательные поля, 405, 404, num_cpu > 0, goroutines > 0, uptime >= 0
- `go/go.mod` — модуль go-info, go 1.22, без зависимостей
- `go/Dockerfile` — двухстадийная сборка: golang:1.22 (тесты + CGO_ENABLED=0 static build) → scratch
- `go/.dockerignore`
- Все тесты проходят (`go test ./... -v`): **53 passed**

---

## М5

**Количество промптов:** 1
**Дата выполнения:** 2026-04-09

### Промпт

Задание М5: docker-compose.yml для трёх сервисов (Python, Go, Rust).
python-app :5005, go-info :8080, rust-textutil (одноразовый). Сеть lab11-net bridge.
Healthcheck у python-app и go-info. Не менее 15 pytest-тестов структуры через PyYAML.

### Результат

Созданы файлы:
- `docker-compose.yml` — три сервиса в сети lab11-net, healthcheck у python-app и go-info, restart: unless-stopped / "no", environment PORT=8080 у go-info
- `tests/test_compose.py` — 26 тестов: наличие сервисов, сеть, порты, healthcheck, restart policy, build contexts, environment, command
- `tests/requirements.txt` — pytest + PyYAML
- Все тесты проходят (`pytest tests/ -v`): **26 passed**

---

## Н3

**Количество промптов:** 1
**Дата выполнения:** 2026-04-09

### Промпт

Задание Н3: CI/CD GitHub Actions для Python, Go и Rust.
4 параллельных тестовых job + build-and-push после всех тестов (только push).
Кеш cargo для Rust. Публикация трёх образов на Docker Hub через secrets.

### Результат

Создан `.github/workflows/ci.yml`:
- `test-python` — setup-python 3.12, pip install, pytest
- `test-go` — setup-go 1.22, go test
- `test-rust` — cargo test с кешем ~/.cargo и rust/target
- `test-compose` — pytest tests/ через PyYAML
- `build-and-push` — docker/login-action + setup-buildx + build-push-action для трёх образов; запускается только при push после успеха всех тестов
- Бейдж CI/CD добавлен в README
