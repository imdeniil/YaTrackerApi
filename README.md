# YaTrackerApi

Асинхронный Python клиент для Yandex Tracker API с модульной архитектурой.

[![Python](https://img.shields.io/pypi/pyversions/YaTrackerApi.svg)](https://pypi.org/project/YaTrackerApi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Установка

```bash
pip install YaTrackerApi
```

Или через `uv`:

```bash
uv add YaTrackerApi
```

## Быстрый старт

```python
import asyncio
from YaTrackerApi import YandexTrackerClient

async def main():
    async with YandexTrackerClient(
        oauth_token="your_oauth_token",
        org_id="your_org_id"
    ) as client:
        # Создание задачи
        issue = await client.issues.create(
            summary="Новая задача",
            queue="DEV",
            description="Описание задачи"
        )
        print(f"Создана: {issue['key']}")

        # Поиск задач
        issues = await client.issues.search(
            filter={"queue": "DEV", "assignee": "me()"},
            per_page=50
        )

asyncio.run(main())
```

### Переменные окружения

Создайте `.env` в корне проекта:

```env
TRACKER_API_KEY=your_oauth_token
TRACKER_ORG_ID=your_org_id
```

```python
from dotenv import load_dotenv
import os

load_dotenv()

async with YandexTrackerClient(
    oauth_token=os.getenv("TRACKER_API_KEY"),
    org_id=os.getenv("TRACKER_ORG_ID")
) as client:
    ...
```

## Структура API

Все модули доступны через свойства клиента. Загружаются лениво — только при первом обращении.

| Модуль | Доступ | Описание |
|--------|--------|----------|
| Задачи | `client.issues` | CRUD, поиск, подсчёт задач |
| Сущности | `client.entities` | Проекты, портфели, цели |
| Очереди | `client.queues` | Управление очередями |
| Пользователи | `client.users` | Информация о пользователях |
| Доски | `client.boards` | Доски, колонки, спринты |
| Компоненты | `client.components` | Компоненты и права доступа |
| Автоматизации | `client.automations` | Макросы, автодействия, триггеры |
| Фильтры | `client.filters` | Сохранённые фильтры |
| Дашборды | `client.dashboards` | Дашборды и виджеты |
| Учёт времени | `client.worklog` | Записи о затраченном времени |
| Импорт | `client.imports` | Импорт задач, комментариев, файлов |
| Внешние связи | `client.external` | Внешние приложения и связи |

## Задачи (`client.issues`)

### CRUD

```python
# Создать задачу
issue = await client.issues.create(
    summary="Новая задача",
    queue="DEV",
    description="Описание",
    assignee="username",
    type="bug",
    priority="critical",
    tags=["backend", "urgent"]
)

# Получить задачу
issue = await client.issues.get("DEV-123")
issue = await client.issues.get("DEV-123", expand="transitions")

# Обновить задачу
await client.issues.update(
    "DEV-123",
    summary="Новое название",
    priority="normal",
    tags={"add": ["new_tag"], "remove": ["old_tag"]}
)

# Переместить задачу
await client.issues.move("DEV-123", queue="NEWQUEUE")
```

### Поиск и подсчёт

```python
# Поиск с фильтром
issues = await client.issues.search(
    filter={"queue": "DEV", "status": "open"},
    order="+created",
    per_page=50
)

# Поиск по запросу
issues = await client.issues.search(
    query="Queue: DEV AND Status: Open"
)

# Подсчёт
count = await client.issues.count(filter={"queue": "DEV"})
```

### Комментарии (`client.issues.comments`)

```python
comments = await client.issues.comments.list("DEV-123")

comment = await client.issues.comments.create(
    "DEV-123", text="Готово", summonees=["user1"]
)

await client.issues.comments.update("DEV-123", comment_id, text="Обновлено")
await client.issues.comments.delete("DEV-123", comment_id)
```

### Вложения (`client.issues.attachments`)

```python
attachments = await client.issues.attachments.list("DEV-123")

att = await client.issues.attachments.attach(
    "DEV-123", file_data=b"content", filename="report.txt"
)

data = await client.issues.attachments.download("DEV-123", att_id, "report.txt")

await client.issues.attachments.delete("DEV-123", att_id)
```

### Чеклисты (`client.issues.checklists`)

```python
checklist = await client.issues.checklists.list("DEV-123")

await client.issues.checklists.create("DEV-123", text="Сделать ревью")

# Обновить/удалить пункт
await client.issues.checklists.item.update(
    "DEV-123", item_id, text="Обновлено", checked=True
)
await client.issues.checklists.item.delete("DEV-123", item_id)

# Удалить весь чеклист
await client.issues.checklists.delete("DEV-123")
```

### Связи (`client.issues.links`)

```python
links = await client.issues.links.list("DEV-123")

link = await client.issues.links.create("DEV-123", "relates", "DEV-456")

await client.issues.links.delete("DEV-123", link_id)
```

### Переходы (`client.issues.transitions`)

```python
transitions = await client.issues.transitions.list("DEV-123")

await client.issues.transitions.execute("DEV-123", "resolve")
```

### Массовые операции (`client.issues.bulk`)

```python
await client.issues.bulk.move(
    issues=["DEV-1", "DEV-2"],
    queue="NEWQUEUE"
)

await client.issues.bulk.update(
    issues=["DEV-1", "DEV-2"],
    priority="critical"
)
```

### Типы, статусы, резолюции, приоритеты

```python
types = await client.issues.types.list()
await client.issues.types.create(key="myType", name={"ru": "Мой тип"})

statuses = await client.issues.statuses.list()
await client.issues.statuses.create(key="review", name={"ru": "Ревью"}, type="inProgress")

resolutions = await client.issues.resolutions.list()
priorities = await client.issues.priorities.list()
```

### Поля (`client.issues.fields`)

```python
# Глобальные поля
fields = await client.issues.fields.list()
field = await client.issues.fields.get("summary")

await client.issues.fields.create(
    name={"ru": "Моё поле"},
    id="myField",
    category=category_id,
    type="ru.yandex.startrek.core.fields.StringFieldType"
)

# Категории полей
category = await client.issues.fields.create_category(
    name={"ru": "Моя категория"}, order=100
)

# Локальные поля очереди
local = await client.issues.fields.local.list("DEV")
field = await client.issues.fields.local.get("DEV", field_key)
await client.issues.fields.local.create(queue_id="DEV", name={"ru": "Поле"}, ...)
```

## Сущности (`client.entities`)

Проекты, портфели, цели.

```python
# CRUD
project = await client.entities.create(
    entity_type="project",
    summary="Новый проект",
    description="Описание"
)

entity = await client.entities.get(
    entity_type="project",
    entity_id=project_id,
    fields="summary,description,lead"
)

await client.entities.update(
    entity_type="project",
    entity_id=project_id,
    summary="Обновлённый проект"
)

await client.entities.delete(entity_type="project", entity_id=project_id)

# Поиск
result = await client.entities.search(
    entity_type="project", input="поисковый запрос", fields="summary"
)

# История изменений
changelog = await client.entities.changelog(
    entity_type="project", entity_id=project_id
)
```

### Подмодули сущностей

```python
# Комментарии
await client.entities.comments.create(entity_type, entity_id, text="...")
comments = await client.entities.comments.list(entity_type, entity_id)

# Чеклисты
await client.entities.checklists.create(entity_type, entity_id, text="Пункт")
await client.entities.checklists.item.update(entity_type, entity_id, item_id, checked=True)

# Связи
await client.entities.links.create(entity_type, entity_id, relationship="depends on", entity=other_id)
links = await client.entities.links.get(entity_type, entity_id)

# Вложения
await client.entities.attachments.attach(entity_type, entity_id, file_id=temp_file_id)
files = await client.entities.attachments.list(entity_type, entity_id)

# Массовое обновление
await client.entities.bulk.update(
    entity_type="project",
    entity_ids=[id1, id2],
    fields={"description": "Новое описание"}
)

# Настройки доступа
settings = await client.entities.settings.get(entity_type, entity_id)

# Ключевые результаты (для целей)
await client.entities.update_key_results(
    entity_id=goal_id,
    key_result_items={"add": {"type": "binary", "text": "Запустить MVP"}}
)

# Метрики
await client.entities.update_metrics(
    entity_type="project", entity_id=project_id,
    metric_items={"add": {"text": "Метрика"}}
)
```

## Очереди (`client.queues`)

```python
queues = await client.queues.list()
queue = await client.queues.get("DEV", expand="all")

new_queue = await client.queues.create(
    key="DESIGN",
    name="Дизайн",
    lead="user_id",
    default_type="task",
    default_priority="normal",
    issue_types_config=[
        {"issueType": "task", "workflow": "W4", "resolutions": ["wontFix"]}
    ]
)

await client.queues.delete("DESIGN")
await client.queues.restore("DESIGN")

# Версии
versions = await client.queues.versions.list("DEV")
await client.queues.versions.create(queue="DEV", name="v2.0")

# Поля и теги
fields = await client.queues.fields.list("DEV")
tags = await client.queues.tags.list("DEV")
await client.queues.tags.delete("DEV", "old_tag")

# Права доступа
perms = await client.queues.permissions.get_user("DEV", user_id)
perms = await client.queues.permissions.get_group("DEV", group_id)
```

## Пользователи (`client.users`)

```python
myself = await client.users.get_myself()
myself = await client.users.get_myself(expand="groups")

user = await client.users.get(uid)
user = await client.users.get("login")

users = await client.users.list()
users = await client.users.list(per_page=10, email="user@example.com")

result = await client.users.get_paginated(per_page=10)
```

## Доски (`client.boards`)

```python
boards = await client.boards.list()
boards = await client.boards.list_paginated(per_page=10)

board = await client.boards.create(
    name="Спринт-доска",
    board_permissions_template="private",
    columns=[
        {"name": "Open", "statuses": ["open"]},
        {"name": "In Progress", "statuses": ["inProgress"]},
        {"name": "Done", "statuses": ["closed"]}
    ]
)

board = await client.boards.get(board_id)
await client.boards.update(board_id, name="Новое имя")
await client.boards.delete(board_id)

# Колонки
columns = await client.boards.columns.list(board_id)
col = await client.boards.columns.create(board_id, name="Review", statuses=["needInfo"])
await client.boards.columns.update(board_id, col_id, name="Code Review")
await client.boards.columns.delete(board_id, col_id)

# Спринты
sprints = await client.boards.sprints.list(board_id)
sprint = await client.boards.sprints.create(
    name="Sprint 1", board_id=board_id,
    start_date="2026-04-01", end_date="2026-04-14"
)
sprint = await client.boards.sprints.get(sprint_id)
```

## Компоненты (`client.components`)

```python
components = await client.components.list()

comp = await client.components.create(
    name="Фронтенд", queue="DEV", description="UI компонент"
)

await client.components.update(comp_id, version=comp['version'], name="Новое имя")

# Права доступа
perms = await client.components.permissions.get_user(comp_id, user_id)
perms = await client.components.permissions.get_group(comp_id, group_id)
```

## Автоматизации (`client.automations`)

```python
# Макросы
macros = await client.automations.macros.list("DEV")
macro = await client.automations.macros.create(
    queue="DEV", name="Мой макрос", body="Комментарий от {{currentUser}}"
)
await client.automations.macros.update("DEV", macro_id, name="Новое имя")
await client.automations.macros.delete("DEV", macro_id)

# Автодействия
autoaction = await client.automations.autoactions.create(
    queue="DEV", name="Авто",
    filter={"priority": ["critical"]},
    actions=[{"type": "Transition", "status": {"key": "needInfo"}}],
    active=False
)
logs = await client.automations.autoactions.get_logs("DEV", autoaction_id)

# Триггеры
trigger = await client.automations.triggers.create(
    queue="DEV", name="Триггер",
    actions=[{"type": "CreateComment", "text": "Сработал!", "fromRobot": True}],
    conditions=[{"type": "Event.create"}],
    active=False
)
```

## Фильтры (`client.filters`)

```python
f = await client.filters.create(
    name="Мои задачи",
    filter={"queue": "DEV", "assignee": "me()"}
)

f = await client.filters.get(filter_id)
await client.filters.update(filter_id, name="Новое имя", query="Queue: DEV")
await client.filters.delete(filter_id)
```

## Дашборды (`client.dashboards`)

```python
dashboard = await client.dashboards.create(name="Аналитика", layout="two-columns")

widget = await client.dashboards.create_cycle_time_widget(
    dashboard_id=dashboard['id'],
    description="Cycle Time",
    query="Queue: DEV",
    from_statuses=[{"key": "open"}],
    to_statuses=[{"key": "closed"}],
    bucket={"unit": "weeks", "count": 1},
    start="now()-3M",
    end="now()"
)
```

## Учёт времени (`client.worklog`)

```python
entry = await client.worklog.create(
    issue_id="DEV-123",
    start="2026-03-01T10:00:00.000+0300",
    duration="PT2H30M",
    comment="Разработка"
)

worklogs = await client.worklog.list("DEV-123")

found = await client.worklog.search(
    created_by="user_id",
    created_at_from="2026-03-01T00:00:00.000+0000"
)

await client.worklog.update("DEV-123", entry_id, duration="PT3H")
await client.worklog.delete("DEV-123", entry_id)
```

## Импорт (`client.imports`)

```python
issue = await client.imports.issue(
    queue="DEV",
    summary="Импортированная задача",
    created_at="2025-01-15T10:00:00.000+0300",
    created_by="user_id"
)

await client.imports.comment(
    issue_id=issue['key'],
    text="Импортированный комментарий",
    created_at="2025-01-15T10:00:00.000+0300",
    created_by="user_id"
)

await client.imports.link(
    issue_id=issue['key'],
    relationship="relates",
    issue="DEV-456",
    created_at="2025-01-15T10:00:00.000+0300",
    created_by="user_id"
)

await client.imports.file(
    issue_id=issue['key'],
    file_data=b"content",
    filename="data.txt",
    created_at="2025-01-15T10:00:00.000+0300",
    created_by="user_id"
)
```

## Внешние связи (`client.external`)

```python
apps = await client.external.links.get_applications()

links = await client.external.links.list("DEV-123")

link = await client.external.links.create(
    issue_id="DEV-123",
    relationship="RELATES",
    key="EXT-001",
    origin="com.gitlab"
)

await client.external.links.delete("DEV-123", link_id)
```

## Обработка ошибок

Все ошибки API наследуются от `TrackerAPIError`:

```python
from YaTrackerApi import (
    TrackerAPIError,
    NotFoundError,
    BadRequestError,
    ForbiddenError,
    UnprocessableEntityError,
    TooManyRequestsError,
)

try:
    issue = await client.issues.get("NONEXISTENT-99999")
except NotFoundError as e:
    print(f"Не найдено: {e.status_code}")  # 404
    print(f"URL: {e.url}")
    print(f"Метод: {e.method}")
    print(f"Ошибки: {e.error_messages}")
except TrackerAPIError as e:
    print(f"Ошибка API: {e.status_code}")
```

| Исключение | HTTP код | Описание |
|------------|----------|----------|
| `BadRequestError` | 400 | Неверные параметры |
| `UnauthorizedError` | 401 | Не авторизован |
| `ForbiddenError` | 403 | Недостаточно прав |
| `NotFoundError` | 404 | Объект не найден |
| `ConflictError` | 409 | Конфликт версий |
| `UnprocessableEntityError` | 422 | Ошибка валидации |
| `LockedError` | 423 | Объект заблокирован |
| `TooManyRequestsError` | 429 | Лимит запросов |
| `ServerError` | 5xx | Ошибка сервера |

## Тесты

Тесты — интеграционные, работают с реальным API. По умолчанию `pytest` их не запускает.

```bash
# Запуск всех интеграционных тестов
uv run pytest -m integration -v

# Только тесты задач
uv run pytest tests/issues/ -m integration -v

# Только конкретный тест
uv run pytest tests/test_users.py -m integration -v
```

Для запуска нужны переменные `TRACKER_API_KEY` и `TRACKER_ORG_ID` в `.env`.

## Особенности и подводные камни

### Пагинация `entities.search()`

Возвращает словарь `{"hits": N, "pages": N, "values": [...]}`, а не список:

```python
result = await client.entities.search(entity_type="project", fields="summary")
projects = result.get("values", [])
total = result.get("hits", 0)
```

### Параметр `fields` для сущностей

Без `fields` API возвращает только базовые данные. Такие поля как `description`, `lead`, `teamUsers`, `parentEntity` **не включаются** по умолчанию:

```python
# Неправильно — summary может отсутствовать
entity = await client.entities.get(entity_type="project", entity_id=id)

# Правильно — явно указываем нужные поля
entity = await client.entities.get(
    entity_type="project", entity_id=id,
    fields="summary,description,lead,teamAccess"
)
```

При использовании `fields` данные находятся в подобъекте `fields`:

```python
summary = entity.get("fields", {}).get("summary", "")
```

### Формат `type` и `priority` при создании задач

API ожидает ключи (`key` или `id`), а не полные объекты:

```python
# Неправильно — полный объект
await client.issues.create(queue="DEV", summary="...", type=issue["type"])

# Правильно — только ключ
await client.issues.create(queue="DEV", summary="...", type="bug")
```

### Формат поля `project` при создании задачи

API ожидает `shortId` (число), а не полный строковый `id`:

```python
project = await client.entities.create(entity_type="project", summary="Проект")
short_id = project.get("shortId")  # число, например 342

# v3 API
await client.issues.create(
    queue="DEV", summary="Задача",
    project={"primary": short_id}
)
```

### Автоконвертация snake_case → camelCase

Параметры автоматически конвертируются:

```python
per_page=50       # → perPage=50
start_date="..."  # → startDate="..."
```

### Оптимистичная блокировка (`version`)

Обновление полей, категорий и компонентов требует параметра `version`. Без него API возвращает **428 Precondition Required**:

```python
field = await client.issues.fields.get("myField")
version = str(field.get("version", "1"))

updated = await client.issues.fields.update(
    field_id="myField", version=version,
    name={"ru": "Новое имя"}
)
```

Версия увеличивается при каждом обновлении. При конфликте — **409 Conflict**.

### Неудаляемые сущности

Через API **нельзя удалить**: задачи (только закрыть), глобальные/локальные поля (только скрыть через `hidden=True`), категории полей, очереди (только через веб-интерфейс).

**Можно удалить**: комментарии, вложения, чеклисты, связи, сущности (проекты/портфели/цели).

### Версии API: v2 и v3

Большинство эндпоинтов используют v3, но фильтры работают на **v2**. Библиотека обрабатывает это автоматически — `FiltersAPI` подменяет `base_url` на `/v2`.

### Перенос задач (`move`)

`issues.move()` может вернуть **422**, если статус задачи не существует в целевой очереди. Используйте массовый перенос со сбросом статуса:

```python
await client.issues.bulk.move(
    queue="TARGET", issues=["DEV-1"],
    initial_status=True  # сбрасывает статус на начальный
)
```

### Загрузка файлов

При загрузке файлов библиотека автоматически создаёт отдельную HTTP сессию без `Content-Type: application/json`, чтобы aiohttp корректно установил `multipart/form-data`.

Миниатюры (`download_thumbnail`) доступны **только для изображений** (.jpg, .png, .gif). Для других типов файлов вернётся 404.

### Чеклисты

- Редактирование пункта — только **PATCH** (не PUT)
- Для сущностей: ответ `checklists.create()` **не содержит** ID пунктов. Нужен отдельный запрос:
  ```python
  entity = await client.entities.get(
      entity_type="project", entity_id=pid, fields="checklistItems"
  )
  items = entity.get("fields", {}).get("checklistItems", [])
  ```
- Удаление всего чеклиста сущности работает **только для project и portfolio** (не для goal — удаляйте пункты по одному)

### Файлы к сущностям: двухшаговый процесс

В отличие от задач, для сущностей нужно сначала загрузить временный файл, затем прикрепить его:

```python
# Шаг 1: загрузка
temp = await client.issues.attachments.upload_temp(
    file_data=b"content", filename="report.txt"
)

# Шаг 2: прикрепление
await client.entities.attachments.attach(
    entity_type="project", entity_id=project_id,
    file_id=str(temp["id"])
)
```

### Ключевые результаты и метрики

Управляются через PATCH основной сущности, отдельных CRUD-эндпоинтов нет. KR доступны **только для целей**, метрики — для всех типов сущностей.

### Колонки доски: `If-Match` в кавычках

Операции с колонками требуют заголовок `If-Match` со значением **в двойных кавычках** (`'"3"'`). Библиотека делает это автоматически.

### Компоненты: кэш `get_all()`

`GET /components` может не содержать только что созданный компонент. При обновлении сразу после создания **всегда передавайте `version` из ответа create**:

```python
comp = await client.components.create(name="New", queue="DEV")
await client.components.update(
    comp["id"], version=comp["version"], name="Updated"
)
```

### Удаление тега из очереди

`tags.delete()` вернёт **422**, если тег используется задачами. Сначала уберите тег со всех задач.

### Создание очереди: валидный workflow

В `issue_types_config` нужно указать существующий ID workflow (например `"W4"`). Получить валидные ID можно из существующей очереди:

```python
queue = await client.queues.get("DEV", expand="all")
for config in queue.get("issueTypesConfig", []):
    print(config.get("workflow", {}).get("id"))  # "W4"
```

### Создание доски

Для создания используется эндпоинт `/liveBoards/` (не `/boards/`). Библиотека обрабатывает это автоматически через `client.boards.create()`.

### Импорт: часовые пояса `createdAt`

API конвертирует даты в UTC перед валидацией. `createdAt` импортируемых комментариев, связей и файлов должен попадать в интервал `[createdAt, updatedAt]` задачи **в UTC**. Используйте единый часовой пояс (рекомендуется `+0000`):

```python
TIMESTAMP = "2025-01-15T07:00:00.000+0000"

issue = await client.imports.issue(
    queue="DEV", summary="Test",
    created_at=TIMESTAMP, created_by=user_id
)
await client.imports.comment(
    issue_id=issue["key"], text="Comment",
    created_at=TIMESTAMP, created_by=user_id
)
```

Для связей `createdAt` должен попадать в интервал **обеих** связанных задач.

### Системные поля

`createdBy`, `createdAt`, `author` — **нельзя изменить** через API. Устанавливаются автоматически на основе OAuth-токена. При клонировании копируйте `lead`/`assignee`/`followers`, а не автора.

### Debug-логирование

```python
import logging
logging.getLogger("YaTrackerApi").setLevel(logging.DEBUG)
```

## Требования

- Python 3.9+
- aiohttp >= 3.12
- python-dotenv >= 1.1

## Лицензия

[MIT](LICENSE)

## Контакты

- GitHub: [@imdeniil](https://github.com/imdeniil)
- Email: keemor821@gmail.com
