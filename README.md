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
