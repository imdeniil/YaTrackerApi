## API для работы с сущностями (Entities)

### 📁 Основные операции с сущностями

#### Создание сущностей (create())
**Обязательные параметры:**
- `entity_type` - тип сущности ("project", "portfolio", "goal")
- `summary` - название сущности

**Опциональные параметры:**
- `lead`, `access`, `description`, `markup_type`, `author`
- `team_users`, `clients`, `followers`, `start`, `end`, `tags`
- `parent_entity`, `entity_status`, `links`

```python
# Создание проекта
project = await client.entities.create(
    entity_type="project",
    summary="Новый проект 2025",
    lead="manager",
    description="Описание проекта"
)

# Создание портфеля с полной настройкой
portfolio = await client.entities.create(
    entity_type="portfolio",
    summary="Портфель проектов 2025",
    team_users=["user1", "user2"],
    start="2025-01-01T00:00:00.000+0300",
    end="2025-12-31T23:59:59.000+0300",
    tags=["strategic", "2025"]
)
```

#### Получение сущностей (get())
**Обязательные параметры:**
- `entity_type`, `entity_id` - ID или shortId сущности

**Опциональные параметры:**
- `fields` - дополнительные поля (строка через запятую)
- `expand` - дополнительная информация ("attachments")

```python
# Базовая информация
project = await client.entities.get("project", "PROJECT-123")

# С дополнительными полями
portfolio = await client.entities.get(
    entity_type="portfolio",
    entity_id="PORTFOLIO-456",
    fields="summary,teamAccess,description,tags",
    expand="attachments"
)
```

#### Обновление сущностей (update())
**Обязательные параметры:**
- `entity_type`, `entity_id`

**Поддерживаемые поля:**
- `summary`, `description`, `lead`, `entity_status`
- `start`, `end`, `tags`, `team_users`, `clients`

```python
await client.entities.update(
    entity_type="project",
    entity_id="PROJECT-123",
    entity_status="completed",
    tags=["completed", "2025"]
)
```

#### Удаление сущностей (delete())
**Параметры:**
- `entity_type`, `entity_id`
- `with_board` - удалить вместе с доской (bool)

```python
# Простое удаление
await client.entities.delete("project", "PROJECT-123")

# Удаление с доской
await client.entities.delete("portfolio", "PORTFOLIO-456", with_board=True)
```

### 🔍 Поиск сущностей (search())
**Обязательные параметры:**
- `entity_type` - тип сущности

**Параметры запроса:**
- `fields`, `per_page`, `page` - настройки ответа

**Параметры фильтрации:**
- `input` - подстрока в названии
- `filter` - параметры фильтрации
- `order_by`, `order_asc` - сортировка
- `root_only` - только корневые сущности

```python
# Простой поиск
projects = await client.entities.search("project")

# Поиск с фильтром
filtered_projects = await client.entities.search(
    entity_type="project",
    filter={"author": "username", "entityStatus": "in_progress"},
    fields="entityStatus,summary,description"
)

# Поиск с пагинацией
portfolios = await client.entities.search(
    entity_type="portfolio",
    input="2025",
    per_page=20,
    page=2,
    order_by="createdAt",
    order_asc=False
)
```

### 📊 История изменений (changelog())
**Обязательные параметры:**
- `entity_type`, `entity_id`

**Параметры пагинации:**
- `per_page`, `from_event`, `selected`, `new_events_on_top`, `direction`

```python
# История изменений проекта
changelog = await client.entities.changelog("project", "PROJECT-123")

# Последние изменения
recent_changes = await client.entities.changelog(
    entity_type="portfolio",
    entity_id="PORTFOLIO-456",
    per_page=20,
    new_events_on_top=True
)
```

### 🔗 Управление связями (links)

#### Создание связей (links.create())
```python
# Зависимость между проектами
await client.entities.links.create(
    entity_type="project",
    entity_id="PROJECT-123",
    relationship="depends on",
    entity="PROJECT-456"
)

# Связь проекта с целью
await client.entities.links.create(
    entity_type="project",
    entity_id="PROJECT-123",
    relationship="works towards",
    entity="GOAL-789"
)
```

#### Получение связей (links.get())
```python
# Все связи проекта
links = await client.entities.links.get("project", "PROJECT-123")

# С дополнительными полями
links = await client.entities.links.get(
    entity_type="portfolio",
    entity_id="PORTFOLIO-456",
    fields="summary,entityStatus,lead"
)
```

#### Удаление связей (links.delete())
```python
await client.entities.links.delete(
    entity_type="project",
    entity_id="PROJECT-123",
    right="PROJECT-456"
)
```

### 📝 Управление чеклистами (checklists)

#### Создание пункта (checklists.create())
**Обязательные параметры:**
- `entity_type`, `entity_id`, `text`

**Опциональные параметры:**
- `checked`, `assignee`, `deadline`
- `notify`, `notify_author`, `fields`, `expand`

```python
# Простое создание
await client.entities.checklists.create(
    entity_type="project",
    entity_id="PROJECT-123",
    text="Подготовить техническое задание"
)

# С дедлайном и исполнителем
await client.entities.checklists.create(
    entity_type="goal",
    entity_id="GOAL-789",
    text="Завершить MVP",
    assignee="developer123",
    deadline={
        "date": "2025-12-31T23:59:59.000+0300",
        "deadlineType": "date"
    }
)
```

#### Массовое обновление (checklists.update())
```python
await client.entities.checklists.update(
    entity_type="project",
    entity_id="PROJECT-123",
    checklist_items=[
        {
            "id": "item_01",
            "text": "Обновленное задание",
            "checked": True,
            "assignee": "new_assignee"
        }
    ]
)
```

#### Управление отдельными пунктами (checklists.item)

**Обновление пункта:**
```python
await client.entities.checklists.item.update(
    entity_type="project",
    entity_id="PROJECT-123",
    checklist_item_id="item_123",
    text="Обновленный текст",
    checked=True
)
```

**Перемещение пункта:**
```python
await client.entities.checklists.item.move(
    entity_type="project",
    entity_id="PROJECT-123",
    checklist_item_id="item_move",
    before="item_target"
)
```

**Удаление пункта:**
```python
await client.entities.checklists.item.delete(
    entity_type="project",
    entity_id="PROJECT-123",
    checklist_item_id="item_123"
)
```

### 🔄 Массовые операции (bulk)

#### Массовое обновление (bulk.update())
**Обязательные параметры:**
- `entity_type`, `entity_ids` - список ID сущностей

**Опциональные параметры:**
- `fields` - поля для обновления
- `comment` - комментарий к операции
- `links` - связи для установки

```python
# Простое массовое обновление
await client.entities.bulk.update(
    entity_type="project",
    entity_ids=["PROJECT-123", "PROJECT-124"],
    fields={"entityStatus": "in_progress"},
    comment="Перевод в работу"
)

# С установкой связей
await client.entities.bulk.update(
    entity_type="portfolio",
    entity_ids=["PORTFOLIO-456"],
    fields={"lead": "new_manager"},
    links=[{"relationship": "depends on", "entity": "GOAL-789"}]
)
```