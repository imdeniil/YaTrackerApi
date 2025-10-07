## API для работы с задачами (Issues)

### 📖 Основные операции

#### Получение задачи (get())
**Обязательные параметры:**
- `issue_id` - идентификатор или ключ задачи (строка)

**Опциональные параметры:**
- `expand` - дополнительные поля (строка или массив): `"transitions"`, `"attachments"`

```python
# Получение базовой информации
issue = await client.issues.get("JUNE-3")

# С дополнительными полями
issue = await client.issues.get("TASK-123", expand=["transitions", "attachments"])
```

#### Создание задачи (create())
**Обязательные параметры:**
- `summary` - название задачи (строка)
- `queue` - очередь для создания (QueueType)

**Основные поля:**
- `description`, `parent`, `markup_type`, `issue_type`, `priority`
- `assignee`, `author`, `sprint`, `followers`, `project`
- `tags`, `unique`, `attachment_ids`, `localfields`

```python
# Минимальное создание
task = await client.issues.create(
    summary="Новая задача",
    queue="DEVELOPMENT"
)

# Полное создание
task = await client.issues.create(
    summary="Интеграция с API",
    queue="DEVELOPMENT",
    description="Реализовать интеграцию с внешним API",
    assignee="developer",
    priority="major",
    tags=["api", "integration"],
    localfields={"estimatedHours": 8}
)
```

#### Обновление задачи (update())
**Обязательные параметры:**
- `issue_id` - идентификатор задачи

**Поддерживает операции add/remove:**
- `followers` - `{"add": ["user1"], "remove": ["user2"]}`
- `tags` - `{"add": ["tag1"], "remove": ["tag2"]}`
- `project.secondary` - `{"add": [123], "remove": [456]}`

```python
# Простое обновление
await client.issues.update("TASK-123", assignee="newuser", priority="critical")

# С операциями add/remove
await client.issues.update(
    issue_id="TASK-123",
    tags={"add": ["urgent"], "remove": ["draft"]},
    followers={"add": ["manager"]}
)
```

#### Перенос задачи (move())
**Обязательные параметры:**
- `issue_id`, `queue` - целевая очередь

**Опциональные параметры:**
- `notify_users`, `initial_status`, `move_all_links`, `expand`

```python
await client.issues.move("TASK-123", queue="TESTING", notify_users=True)
```

### 🔍 Поиск и аналитика

#### Поиск задач (search())
**Основные параметры:**
- `filter` - фильтр поиска (строка или объект)
- `query` - текстовый поиск
- `order`, `order_asc` - сортировка
- `per_page`, `scroll_token` - пагинация

```python
# Поиск по фильтру
issues = await client.issues.search(filter="assignee: me() AND status: open")

# Сложный поиск
issues = await client.issues.search(
    filter="status: !closed AND priority: critical",
    order="updated",
    order_asc=False,
    per_page=20,
    expand="attachments"
)
```

#### Подсчет задач (count())
```python
count = await client.issues.count(filter="assignee: me() AND status: open")
```

#### Получение приоритетов (priorities())
```python
priorities = await client.issues.priorities(localized=True)
```

#### История изменений (changelog())
**Параметры пагинации:**
- `per_page`, `from_change_id`, `selected_id`
- `new_events_on_top`, `direction`

```python
# Последние изменения
changes = await client.issues.changelog(
    issue_id="TASK-123",
    per_page=10,
    new_events_on_top=True
)
```

#### Очистка скролл-контекста (clear_scroll())
```python
await client.issues.clear_scroll(scroll_id="scroll_123456")
```

### 🔗 Подмодули

#### Связи между задачами (links)
```python
# Получение связей
links = await client.issues.links.get("TASK-123")

# Создание связи
await client.issues.links.create(
    issue_id="TASK-123",
    relationship="depends on",
    issue="TASK-456"
)

# Удаление связи
await client.issues.links.delete("TASK-123", link_id="link_789")
```

#### Переходы по жизненному циклу (transitions)
```python
# Доступные переходы
transitions = await client.issues.transitions.get("TASK-123")

# Выполнение перехода
await client.issues.transitions.update(
    issue_id="TASK-123",
    transition_id="resolve",
    fields={"resolution": "fixed"}
)
```

#### Чеклисты (checklists)
```python
# Получение чеклистов
checklists = await client.issues.checklists.get("TASK-123")

# Создание пункта
await client.issues.checklists.create(
    issue_id="TASK-123",
    text="Выполнить тестирование"
)

# Удаление всех пунктов
await client.issues.checklists.delete("TASK-123")

# Управление отдельными пунктами
await client.issues.checklists.item.update(
    issue_id="TASK-123",
    checklist_item_id="item_123",
    text="Обновленный текст",
    checked=True
)
```

#### Комментарии (comments)
```python
# Получение комментариев
comments = await client.issues.comments.get("TASK-123", expand="all")

# Создание комментария
await client.issues.comments.create(
    issue_id="TASK-123",
    text="## Статус работы\n**Выполнено:** ✅",
    markup_type="md",
    summonees=["reviewer"]
)

# Обновление комментария
await client.issues.comments.update(
    issue_id="TASK-123",
    comment_id="comment_123",
    text="Исправленный комментарий"
)

# Удаление комментария
await client.issues.comments.delete("TASK-123", "comment_123")
```

#### Поля (fields)
```python
# Получение всех полей
fields = await client.issues.fields.get()

# Создание кастомного поля
await client.issues.fields.create(
    name={"en": "Priority 2025", "ru": "Приоритет 2025"},
    id="priority_2025",
    category="category_id",
    type="ru.yandex.startrek.core.fields.StringFieldType"
)

# Локальные поля очереди
await client.issues.fields.local.create(
    queue_id="TESTQUEUE",
    name={"en": "Local Field", "ru": "Локальное поле"},
    id="local_field_id",
    category="category_id",
    type="ru.yandex.startrek.core.fields.StringFieldType"
)
```