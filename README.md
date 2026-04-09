# Лабораторная работа №11
**Студент:** Фомичев Ярослав Николаевич
**Группа:** 221131
**Вариант:** 1

---

## М1 — Dockerfile для Python-приложения

### Описание сервиса

Flask-приложение с REST API для управления предметами (items) на базе SQLite.
Реализована слоёная архитектура: `routes → services → repositories`.
Основан на Blueprint `item_routes` из ЛР №6.

### Таблица эндпоинтов

| Метод  | URL                        | Описание                  |
|--------|----------------------------|---------------------------|
| GET    | /health                    | Проверка работоспособности |
| GET    | /items/api/items           | Список всех предметов     |
| POST   | /items/api/items           | Создать предмет           |
| GET    | /items/api/items/{id}      | Получить предмет по ID    |
| PUT    | /items/api/items/{id}      | Обновить предмет          |
| DELETE | /items/api/items/{id}      | Удалить предмет           |

### Сборка и запуск

```bash
# Сборка образа
docker build -t lb11-python ./python

# Запуск контейнера
docker run -d -p 5005:5005 --name lb11-python lb11-python
```

### Примеры curl запросов

```bash
# Проверка здоровья
curl http://localhost:5005/health

# Создать предмет
curl -X POST http://localhost:5005/items/api/items \
  -H "Content-Type: application/json" \
  -d '{"title": "Notebook", "description": "A spiral notebook"}'

# Получить все предметы
curl http://localhost:5005/items/api/items

# Получить предмет по ID
curl http://localhost:5005/items/api/items/1

# Обновить предмет
curl -X PUT http://localhost:5005/items/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Notebook", "description": "Updated description"}'

# Удалить предмет
curl -X DELETE http://localhost:5005/items/api/items/1
```

---

## М3 — Dockerfile для Rust-приложения

### Описание утилиты

CLI-инструмент `textutil` для работы с текстом. Принимает команду и аргумент,
возвращает результат в формате JSON. Реализован на чистом Rust без внешних зависимостей.

Команды:
- `count <текст>` — подсчёт слов, символов и строк
- `reverse <текст>` — обратный порядок символов
- `upper <текст>` — преобразование в верхний регистр
- `lower <текст>` — преобразование в нижний регистр

### Сборка и запуск

```bash
# Сборка образа
docker build -t lb11-rust ./rust

# Подсчёт слов/символов/строк
docker run --rm lb11-rust count "hello world"

# Переворот строки
docker run --rm lb11-rust reverse "hello"

# Верхний регистр
docker run --rm lb11-rust upper "hello world"

# Нижний регистр
docker run --rm lb11-rust lower "HELLO WORLD"
```

### Примеры вывода

```bash
$ docker run --rm lb11-rust count "hello world"
{"command":"count","input":"hello world","words":2,"chars":11,"lines":1}

$ docker run --rm lb11-rust reverse "hello"
{"command":"reverse","input":"hello","result":"olleh"}

$ docker run --rm lb11-rust upper "hello world"
{"command":"upper","input":"hello world","result":"HELLO WORLD"}

$ docker run --rm lb11-rust lower "HELLO WORLD"
{"command":"lower","input":"HELLO WORLD","result":"hello world"}
```

---

## Н1 — Go-сервис в scratch-образе

### Описание

HTTP-сервис информации о системе на чистом Go (только stdlib, без зависимостей).
Компилируется статически (`CGO_ENABLED=0`) и упаковывается в `scratch` — итоговый образ
содержит только бинарник (~7 МБ).

### Таблица эндпоинтов

| Метод | URL       | Описание                                       |
|-------|-----------|------------------------------------------------|
| GET   | /         | Сводка сервиса: имя, версия, список маршрутов  |
| GET   | /health   | Статус `ok` + текущее время (RFC3339)          |
| GET   | /info     | hostname, go_version, os, arch, num_cpu        |
| GET   | /metrics  | uptime_seconds, goroutines, alloc_mb, sys_mb   |

При неверном методе → `405 Method Not Allowed` (JSON).
При несуществующем пути → `404 Not Found` (JSON).

### Сборка и запуск

```bash
# Сборка образа (внутри также запускаются тесты)
docker build -t go-info ./go

# Запуск на порту 8080
docker run -d -p 8080:8080 --name go-info go-info

# Запуск на другом порту через переменную окружения
docker run -d -p 9090:9090 -e PORT=9090 --name go-info go-info

# Размер образа
docker images go-info
```

### Примеры curl

```bash
curl http://localhost:8080/
# {"routes":["/","/health","/info","/metrics"],"service":"go-info","version":"1.0.0"}

curl http://localhost:8080/health
# {"status":"ok","timestamp":"2026-04-09T12:00:00Z"}

curl http://localhost:8080/info
# {"arch":"amd64","go_version":"go1.22.0","hostname":"...","num_cpu":8,"os":"linux"}

curl http://localhost:8080/metrics
# {"alloc_mb":0.42,"goroutines":4,"sys_mb":7.21,"uptime_seconds":3.14}
```
