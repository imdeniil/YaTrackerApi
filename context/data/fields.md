## 🏷️ API для работы с полями (Fields)

### 📖 Управление полями

#### Получение полей (get())
```python
# Все поля
fields = await client.issues.fields.get()

# Конкретное поле
field = await client.issues.fields.get("field_id")

# Структура ответа
{
    "id": "field_12345",
    "key": "summary",
    "name": {"ru": "Название"},
    "description": {"ru": "Описание"},
    "type": "string",
    "schema": {
        "type": "string",
        "required": True,
        "readonly": False,
        "maxLength": 255
    },
    "options": [...]  # для списков
}
```

#### Создание кастомных полей (create())
**Обязательные параметры:**
- `name` - двуязычное название {"en": "English", "ru": "Русский"}
- `id` - уникальный идентификатор поля
- `category` - ID категории поля
- `type` - тип поля (8 поддерживаемых типов)

**Опциональные параметры:**
- `options_provider` - для выпадающих списков
- `order`, `description`, `readonly`, `visible`, `hidden`, `container`

```python
await client.issues.fields.create(
    name={"en": "Priority 2025", "ru": "Приоритет 2025"},
    id="priority_2025",
    category="category_id_from_api",
    type="ru.yandex.startrek.core.fields.StringFieldType",
    description="Кастомный приоритет на 2025 год"
)
```

#### Обновление полей (update())
**Обязательные параметры:**
- `field_id`, `version` - для оптимистичной блокировки

**Опциональные параметры:**
- Все остальные параметры из создания

```python
await client.issues.fields.update(
    field_id="custom_field_123",
    version=5,
    name={"en": "Updated Field", "ru": "Обновленное поле"},
    description="Новое описание"
)
```

#### Создание категорий (create_category())
**Обязательные параметры:**
- `name` - двуязычное название
- `order` - вес при отображении

```python
await client.issues.fields.create_category(
    name={"en": "Custom Category", "ru": "Кастомная категория"},
    order=10,
    description="Категория для кастомных полей"
)
```

### 🏢 Локальные поля очередей (LocalFields)

#### Получение локальных полей (local.get())
```python
# Все локальные поля очереди
local_fields = await client.issues.fields.local.get("TESTQUEUE")

# Конкретное локальное поле
field = await client.issues.fields.local.get("TESTQUEUE", "custom_priority_local")
```

#### Создание локальных полей (local.create())
**Обязательные параметры:**
- `queue_id`, `name`, `id`, `category`, `type`

```python
await client.issues.fields.local.create(
    queue_id="TESTQUEUE",
    name={"en": "Local Priority", "ru": "Локальный приоритет"},
    id="local_priority_field",
    category="category_id",
    type="ru.yandex.startrek.core.fields.StringFieldType",
    options_provider={
        "type": "FixedListOptionsProvider",
        "values": ["Высокий", "Средний", "Низкий"]
    }
)
```

#### Обновление локальных полей (local.update())
```python
await client.issues.fields.local.update(
    queue_id="TESTQUEUE",
    field_key="custom_priority_local",
    name={"en": "Updated Local Field", "ru": "Обновленное локальное поле"},
    readonly=True
)
```

### 🔧 Поддерживаемые типы полей

#### Основные типы полей для создания:
1. `ru.yandex.startrek.core.fields.StringFieldType` - Строковое поле
2. `ru.yandex.startrek.core.fields.TextFieldType` - Текстовое поле (многострочное)
3. `ru.yandex.startrek.core.fields.IntegerFieldType` - Целое число
4. `ru.yandex.startrek.core.fields.FloatFieldType` - Десятичное число
5. `ru.yandex.startrek.core.fields.DateFieldType` - Дата
6. `ru.yandex.startrek.core.fields.DateTimeFieldType` - Дата и время
7. `ru.yandex.startrek.core.fields.BooleanFieldType` - Булево значение
8. `ru.yandex.startrek.core.fields.DropDownFieldType` - Выпадающий список

#### Провайдеры опций для выпадающих списков:
```python
# Фиксированный список
options_provider = {
    "type": "FixedListOptionsProvider",
    "values": ["Опция 1", "Опция 2", "Опция 3"]
}

# Пользователи
options_provider = {
    "type": "UserFieldOptionsProvider"
}

# Компоненты
options_provider = {
    "type": "ComponentFieldOptionsProvider"
}
```

### 📋 Примеры использования кастомных полей

```python
# В создании задачи
task = await client.issues.create(
    summary="Задача с кастомными полями",
    queue="DEVELOPMENT",
    localfields={
        "priority_2025": "Критический",
        "business_value": 95,
        "estimated_hours": 16.5,
        "is_urgent": True,
        "deadline_custom": "2025-12-31",
        "tags_internal": ["backend", "api"],
        "metadata": {
            "source": "external_system",
            "version": "2.1.0"
        }
    }
)

# В обновлении задачи
await client.issues.update(
    issue_id="TASK-123",
    localfields={
        "priority_2025": "Высокий",
        "progress_percent": 75
    }
)
```