# YaTrackerApi

> Асинхронный Python клиент для работы с Yandex Tracker API с модульной архитектурой

[![PyPI version](https://badge.fury.io/py/YaTrackerApi.svg)](https://badge.fury.io/py/YaTrackerApi)
[![Python](https://img.shields.io/pypi/pyversions/YaTrackerApi.svg)](https://pypi.org/project/YaTrackerApi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Содержание

- [Особенности](#-особенности)
- [Установка](#-установка)
- [Быстрый старт](#-быстрый-старт)
- [Основные возможности](#-основные-возможности)
  - [Работа с задачами](#работа-с-задачами)
  - [Связи между задачами](#связи-между-задачами)
  - [Управление статусами](#управление-статусами)
  - [Чеклисты](#чеклисты)
  - [Комментарии](#комментарии)
  - [Работа с полями](#работа-с-полями)
  - [Работа с сущностями](#работа-с-сущностями)
  - [Работа с пользователями](#работа-с-пользователями)
  - [Работа с очередями](#работа-с-очередями)
- [API Модули](#-api-модули)
- [Особенности и подводные камни](#-особенности-и-подводные-камни)
- [Требования](#-требования)
- [Лицензия](#-лицензия)
- [Контакты](#-контакты)

## ✨ Особенности

- **Асинхронность** - полная поддержка `async/await` на базе `aiohttp`
- **Модульная архитектура** - логическое разделение функциональности по модулям
- **Lazy Loading** - модули загружаются только при первом обращении
- **Типизация** - полная поддержка типов для всех методов
- **Гибкость** - множественные форматы для одного поля (строки, числа, объекты)
- **Валидация** - проверка данных на стороне клиента перед отправкой
- **Логирование** - система логов на русском языке с настраиваемым уровнем
- **Кастомные поля** - поддержка пользовательских полей любых типов
- **Безопасность** - настроенный SSL/TLS контекст для всех соединений

## 📦 Установка

```bash
pip install YaTrackerApi
```

Или через `uv`:

```bash
uv add YaTrackerApi
```

## 🚀 Быстрый старт

```python
import asyncio
from client import YandexTrackerClient

async def main():
    async with YandexTrackerClient(
        oauth_token="your_oauth_token",
        org_id="your_org_id",
        log_level="INFO"
    ) as client:
        # Создание задачи
        issue = await client.issues.create(
            summary="Новая задача",
            queue="TESTBOT",
            description="Подробное описание задачи"
        )
        print(f"Создана задача: {issue['key']}")

        # Получение задачи
        issue = await client.issues.get('TESTBOT-1')
        print(f"Задача: {issue['summary']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
TRACKER_API_KEY=your_oauth_token
TRACKER_ORG_ID=your_org_id
```

И загрузите их:

```python
from dotenv import load_dotenv
import os

load_dotenv()

async with YandexTrackerClient(
    oauth_token=os.getenv("TRACKER_API_KEY"),
    org_id=os.getenv("TRACKER_ORG_ID")
) as client:
    # ваш код
```

## 💡 Основные возможности

### Работа с задачами

#### Создание задачи

```python
# Простое создание
issue = await client.issues.create(
    summary="Новая задача",
    queue="TESTBOT"
)

# С полными параметрами
issue = await client.issues.create(
    summary="Задача с полными параметрами",
    queue="TESTBOT",
    description="Подробное описание",
    assignee="username",
    priority={"id": "2", "key": "minor"},
    type="bug",
    tags=["backend", "urgent"]
)

# С кастомными полями
issue = await client.issues.create(
    summary="Задача с кастомными полями",
    queue="TESTBOT",
    localfields={
        "numberOfEmployees": 10,
        "contact_cl": "ООО Рога и Копыта",
        "customPriority": "Очень высокий"
    }
)
```

#### Получение задачи

```python
# Базовое получение
issue = await client.issues.get('TESTBOT-1')

# С расширенными полями
issue = await client.issues.get(
    'TESTBOT-1',
    expand=['transitions', 'attachments']
)
```

#### Обновление задачи

```python
# Простое обновление
await client.issues.update(
    issue_id='TESTBOT-1',
    summary="Обновленное название"
)

# Полное обновление
await client.issues.update(
    issue_id='TESTBOT-1',
    summary="Новое название",
    description="Новое описание",
    priority={"id": "1", "key": "critical"},
    assignee="new_assignee",
    tags={"add": ["new_tag"], "remove": ["old_tag"]}
)
```

#### Перенос задачи

```python
# Перенос в другую очередь
issue = await client.issues.move(
    issue_id='TESTBOT-1',
    queue='NEWQUEUE',
    move_all_fields=True,
    initial_status=True
)
```

#### Поиск задач

```python
# Поиск с фильтром
issues = await client.issues.search(
    filter={"queue": "TESTBOT", "assignee": "me()"},
    order="+status",
    expand=["transitions", "attachments"],
    per_page=50
)

# Поиск по текстовому запросу
issues = await client.issues.search(
    query="Queue: TESTBOT AND Status: Open"
)
```

#### Подсчет задач

```python
count = await client.issues.count(
    query="Queue: TESTBOT AND Status: New"
)
print(f"Найдено задач: {count}")
```

#### Получение приоритетов

```python
# Все приоритеты
priorities = await client.issues.priorities()

# Локализованные приоритеты
priorities = await client.issues.priorities(localized=True)
```

#### История изменений

```python
changelog = await client.issues.changelog('TESTBOT-1')
for change in changelog:
    print(f"{change['updatedAt']}: {change['updatedBy']['display']}")
```

### Связи между задачами

```python
# Получение связей
links = await client.issues.links.get('TESTBOT-1')

# Создание связи
await client.issues.links.create(
    issue_id='TESTBOT-1',
    relationship='relates',
    issue='TESTBOT-2'
)

# Удаление связи
await client.issues.links.delete(
    issue_id='TESTBOT-1',
    link_id='12345'
)
```

### Управление статусами

```python
# Получение доступных переходов
transitions = await client.issues.transitions.get('TESTBOT-1')

# Выполнение перехода
await client.issues.transitions.update(
    issue_id='TESTBOT-1',
    transition_id='resolve'
)
```

### Чеклисты

```python
# Получение чеклистов задачи
checklists = await client.issues.checklists.get('TESTBOT-1')

# Создание пункта чеклиста
await client.issues.checklists.create(
    issue_id='TESTBOT-1',
    text='Выполнить задачу',
    checked=False
)

# Создание с дедлайном
await client.issues.checklists.create(
    issue_id='TESTBOT-1',
    text='Подготовить релиз',
    checked=False,
    deadline={
        'date': '2025-12-31T23:59:59.000+0000',
        'deadlineType': 'date'
    }
)

# Обновление пункта чеклиста
await client.issues.checklists.item.update(
    issue_id='TESTBOT-1',
    checklist_item_id='item123',
    text='Обновленный текст',
    checked=True
)

# Удаление пункта
await client.issues.checklists.item.delete(
    issue_id='TESTBOT-1',
    checklist_item_id='item123'
)
```

### Комментарии

```python
# Получение комментариев
comments = await client.issues.comments.get('TESTBOT-1')

# Создание комментария
await client.issues.comments.create(
    issue_id='TESTBOT-1',
    text='Работа завершена',
    summonees=['user1', 'user2']
)

# Обновление комментария
await client.issues.comments.update(
    issue_id='TESTBOT-1',
    comment_id='123',
    text='Обновленный комментарий'
)

# Удаление комментария
await client.issues.comments.delete(
    issue_id='TESTBOT-1',
    comment_id='123'
)
```

### Работа с полями

```python
# Получение всех полей
fields = await client.issues.fields.get()

# Получение конкретного поля
field = await client.issues.fields.get(field_id='customField1')

# Создание кастомного поля
await client.fields.create(
    name="Приоритет проекта",
    key="projectPriority",
    category="0000000000000001",
    type="ru.yandex.startrek.core.fields.StringFieldType"
)

# Обновление поля
await client.fields.update(
    field_id='customField1',
    name="Новое название поля"
)

# Работа с локальными полями очереди
local_fields = await client.fields.local.get(queue_id='TESTBOT')

# Создание локального поля
await client.fields.local.create(
    queue_id='TESTBOT',
    name="Локальное поле",
    key="localField1"
)
```

### Работа с сущностями

Сущности в Yandex Tracker - это проекты, портфели и цели.

```python
# Создание проекта
project = await client.entities.create(
    entity_type="project",
    summary="Новый проект",
    lead="username"
)

# Получение сущности
entity = await client.entities.get(
    entity_id="project123",
    expand=["attachments"]
)

# Обновление сущности
await client.entities.update(
    entity_id="project123",
    summary="Обновленное название проекта"
)

# Поиск сущностей
entities = await client.entities.search(
    entity_type="project",
    filter={"lead": "username"},
    order="+createdAt"
)

# Удаление сущности
await client.entities.delete(
    entity_id="project123",
    withBoard=True  # Удалить вместе с доской
)

# Массовое обновление
await client.entities.bulk.update(
    entity_ids=["project1", "project2"],
    status="active"
)

# Работа со связями сущностей
await client.entities.links.create(
    entity_id="project1",
    relationship="relates",
    entity="project2"
)
```

### Работа с пользователями

```python
# Получение списка всех пользователей
users = await client.users.get()

# Анализ пользователей
for user in users:
    print(f"{user['display']} ({user['login']})")

# Фильтрация активных
active_users = [u for u in users if not u.get('dismissed', False)]

# Получение конкретного пользователя по логину
user = await client.users.get('username')

# Получение пользователя по ID
user = await client.users.get(123456)
```

### Работа с очередями

```python
# Получение списка всех очередей
queues = await client.queues.get()

# Получение конкретной очереди
queue = await client.queues.get('TREK', expand='all')

# Создание очереди
new_queue = await client.queues.create(
    key='DESIGN',
    name='Design Team',
    lead='username',
    default_type='task',
    default_priority='normal',
    issue_types_config=[
        {
            'issueType': 'task',
            'workflow': 'oicn',
            'resolutions': ['wontFix', 'fixed']
        }
    ],
    description='Очередь команды дизайна'
)

# Удаление очереди
await client.queues.delete('OLDQUEUE')

# Восстановление удаленной очереди
restored_queue = await client.queues.restore('OLDQUEUE')

# Работа с версиями очереди
versions = await client.queues.versions.get('TREK')

# Создание версии
version = await client.queues.versions.create(
    queue='TREK',
    name='v2.0.0',
    description='Релиз версии 2.0',
    start_date='2025-01-01',
    due_date='2025-12-31'
)

# Получение полей очереди
fields = await client.queues.fields.get('TREK')

# Получение тегов очереди
tags = await client.queues.tags.get('TREK')

# Удаление тега
await client.queues.tags.delete('TREK', 'deprecated')

# Массовое управление доступом к очереди
await client.queues.bulk.update(
    queue_id='TREK',
    create={'add': ['user1', 'user2']},
    write={'remove': ['user3']}
)

# Получение прав доступа пользователя к очереди
user_access = await client.queues.user.get('TREK', 'username')

# Получение прав доступа группы к очереди
group_access = await client.queues.group.get('TREK', 'group_id')
```

## 🔧 API Модули

Клиент состоит из следующих модулей:

### IssuesAPI (`client.issues`)
Работа с задачами:
- `get()` - получение задачи
- `create()` - создание задачи
- `update()` - обновление задачи
- `move()` - перенос задачи между очередями
- `search()` - поиск задач
- `count()` - подсчет задач
- `priorities()` - получение приоритетов
- `changelog()` - история изменений

**Подмодули:**
- `links` - связи между задачами
- `transitions` - переходы статусов
- `checklists` - чеклисты задач
- `comments` - комментарии
- `fields` - поля задач

### FieldsAPI (`client.fields`)
Управление полями:
- `get()` - получение списка полей
- `create()` - создание кастомного поля
- `update()` - обновление поля
- `create_category()` - создание категории полей

**Подмодуль:**
- `local` - локальные поля очередей

### EntitiesAPI (`client.entities`)
Работа с сущностями (проекты, портфели, цели):
- `get()` - получение сущности
- `create()` - создание сущности
- `update()` - обновление сущности
- `delete()` - удаление сущности
- `search()` - поиск сущностей
- `changelog()` - история изменений

**Подмодули:**
- `checklists` - чеклисты сущностей
- `bulk` - массовые операции
- `links` - связи между сущностями

### UsersAPI (`client.users`)
Работа с пользователями:
- `get()` - получение списка всех пользователей или конкретного пользователя

### QueuesAPI (`client.queues`)
Управление очередями:
- `get()` - получение очереди или списка очередей
- `create()` - создание новой очереди
- `delete()` - удаление очереди
- `restore()` - восстановление удаленной очереди

**Подмодули:**
- `versions` - версии очередей (create, get)
- `fields` - поля очередей (get)
- `tags` - теги очередей (get, delete)
- `bulk` - массовое управление доступом (update)
- `user` - права доступа пользователя (get)
- `group` - права доступа группы (get)

## ⚠️ Особенности и подводные камни

При работе с Yandex Tracker API есть ряд важных нюансов, которые необходимо учитывать для корректной работы.

### 1. Пагинация при поиске сущностей

**Проблема:** `entities.search()` возвращает пагинированный ответ в виде словаря, а не списка.

**Структура ответа:**
```python
{
    "hits": 125,      # Общее количество найденных сущностей
    "pages": 3,       # Количество страниц
    "values": [...]   # Массив сущностей на текущей странице (по умолчанию 50)
}
```

**Решение:**
```python
# Получаем первую страницу
projects_raw = await client.entities.search(
    entity_type="project",
    fields="summary,id"
)

# Проверяем тип ответа и загружаем все страницы
if isinstance(projects_raw, dict):
    pages = projects_raw.get("pages", 1)

    if isinstance(pages, int) and pages > 1:
        per_page = pages * 50
        projects_raw = await client.entities.search(
            entity_type="project",
            fields="summary,id",
            per_page=per_page
        )

    projects = projects_raw.get("values", [])
else:
    projects = projects_raw
```

### 2. Параметр fields при поиске

**Проблема:** Без явного указания полей в параметре `fields`, API может не возвращать важные данные.

**Неправильно:**
```python
projects = await client.entities.search(entity_type="project")
# summary может отсутствовать в ответе
```

**Правильно:**
```python
projects = await client.entities.search(
    entity_type="project",
    fields="summary,id,description"
)

# Извлекаем данные
for proj in projects["values"]:
    summary = proj.get("fields", {}).get("summary", "")
    if not summary:
        summary = proj.get("summary", "")
```

### 3. Формат поля project при создании задачи

**Проблема:** API ожидает `shortId` проекта (число), а не полный `id` (строка).

**Неправильно:**
```python
project = {
    "id": "68e5764ffa5085239cef5e94"  # ❌ Строковый ID
}
```

**Правильно:**
```python
# После создания проекта
new_project = await client.entities.create(
    entity_type="project",
    summary="Новый проект"
)

# Используйте shortId
project_short_id = new_project.get("shortId")

# Создаем задачу
issue = await client.issues.create(
    summary="Задача проекта",
    queue="TESTBOT",
    project={"primary": project_short_id}  # ✅ shortId как число
)
```

### 4. Формат полей type и priority

**Проблема:** API выдает ошибку 400, если передать полные объекты вместо ключей.

**Неправильно:**
```python
issue = await client.issues.get("TESTBOT-1")

new_issue = await client.issues.create(
    summary="Копия",
    queue="TESTBOT",
    type=issue["type"],        # ❌ Полный объект
    priority=issue["priority"]  # ❌ Полный объект
)
```

**Правильно:**
```python
def extract_field_value(field_data):
    """Извлечь значение поля для API запроса"""
    if isinstance(field_data, dict):
        return field_data.get("key") or field_data.get("id")
    return field_data

new_issue = await client.issues.create(
    summary="Копия",
    queue="TESTBOT",
    type=extract_field_value(issue.get("type")),        # ✅ "milestone"
    priority=extract_field_value(issue.get("priority"))  # ✅ "normal"
)
```

### 5. Получение сущностей с полным набором полей

**Проблема:** Без параметра `fields` API возвращает только базовые поля.

**Неправильно:**
```python
project = await client.entities.get(
    entity_id=project_id,
    entity_type="project"
)
# НЕТ: description, lead, teamUsers, parentEntity
```

**Правильно:**
```python
project = await client.entities.get(
    entity_id=project_id,
    entity_type="project",
    fields="summary,description,lead,teamUsers,teamAccess,parentEntity,clients,followers,start,end,tags"
)
# ✅ Все поля присутствуют
```

### 6. Ограничения на изменение системных полей

**Нельзя изменить:**
- ❌ `createdBy` - автор (устанавливается автоматически)
- ❌ `createdAt` - дата создания
- ❌ `author` - автор (алиас createdBy)

**Можно изменить:**
- ✅ `lead` - руководитель проекта
- ✅ `assignee` - исполнитель задачи
- ✅ `teamUsers` - участники
- ✅ `followers` - наблюдатели

```python
# Правильное обновление
await client.entities.update(
    entity_id=project_id,
    lead="user_login",
    teamUsers=["user1", "user2"]
)
```

### Дополнительные замечания

**Автоконвертация параметров:** Библиотека автоматически конвертирует snake_case в camelCase:
```python
per_page=50  # → perPage=50 в API
```

**Обработка ошибок:** Используйте debug логирование для диагностики:
```python
import logging
logging.getLogger("YaTrackerApi").setLevel(logging.DEBUG)
```

Полная документация: [context/gotchas.md](context/gotchas.md)

## 📋 Требования

- Python 3.9+
- aiohttp >= 3.12.15
- python-dotenv >= 1.1.1

## 📄 Лицензия

Проект распространяется под лицензией [MIT](LICENSE).

## 👤 Контакты

**Даниил**

- GitHub: [@imdeniil](https://github.com/imdeniil)
- Email: keemor821@gmail.com

## 🔗 Ссылки

- [PyPI](https://pypi.org/project/YaTrackerApi/)
- [GitHub Repository](https://github.com/imdeniil/YaTrackerApi)
- [Issues](https://github.com/imdeniil/YaTrackerApi/issues)
- [Официальная документация Yandex Tracker API](https://cloud.yandex.ru/docs/tracker/about-api)

---

**Создано с ❤️ для упрощения работы с Yandex Tracker API**
