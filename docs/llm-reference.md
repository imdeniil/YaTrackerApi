# YaTrackerApi — LLM Reference

Асинхронный Python клиент для Yandex Tracker API. Все методы async, клиент используется как async context manager.

```python
from YaTrackerApi import YandexTrackerClient

async with YandexTrackerClient(oauth_token="...", org_id="...") as client:
    ...
```

## Дерево модулей

```
client.issues                          # Задачи
client.issues.comments                 # Комментарии к задачам
client.issues.attachments              # Вложения к задачам
client.issues.checklists               # Чеклисты задач
client.issues.checklists.item          # Пункты чеклиста
client.issues.links                    # Связи задач
client.issues.transitions              # Переходы (смена статуса)
client.issues.bulk                     # Массовые операции
client.issues.fields                   # Глобальные поля
client.issues.fields.local             # Локальные поля очереди
client.issues.types                    # Типы задач
client.issues.statuses                 # Статусы
client.issues.resolutions              # Резолюции
client.issues.priorities               # Приоритеты

client.entities                        # Сущности (project, portfolio, goal)
client.entities.comments               # Комментарии к сущностям
client.entities.attachments            # Вложения к сущностям
client.entities.checklists             # Чеклисты сущностей
client.entities.checklists.item        # Пункты чеклиста сущностей
client.entities.links                  # Связи сущностей
client.entities.bulk                   # Массовое обновление сущностей
client.entities.settings               # Настройки доступа

client.queues                          # Очереди
client.queues.versions                 # Версии очереди
client.queues.fields                   # Поля очереди
client.queues.tags                     # Теги очереди
client.queues.permissions              # Права доступа

client.users                           # Пользователи
client.boards                          # Доски
client.boards.columns                  # Колонки доски
client.boards.sprints                  # Спринты
client.components                      # Компоненты
client.components.permissions          # Права компонентов
client.automations.macros              # Макросы
client.automations.triggers            # Триггеры
client.automations.autoactions         # Автодействия
client.filters                         # Фильтры (API v2)
client.dashboards                      # Дашборды
client.worklog                         # Учёт времени
client.imports                         # Импорт данных
client.external.links                  # Внешние связи
```

---

## Полный справочник методов

### client.issues

```python
await client.issues.get(issue_id, expand=None)
await client.issues.create(summary, queue, parent=None, description=None, markup_type=None, sprint=None, issue_type=None, priority=None, followers=None, assignee=None, author=None, project=None, unique=None, attachment_ids=None, description_attachment_ids=None, tags=None, localfields=None, **kwargs)
await client.issues.update(issue_id, summary=None, description=None, parent=None, markup_type=None, sprint=None, issue_type=None, priority=None, followers=None, project=None, attachment_ids=None, description_attachment_ids=None, tags=None, localfields=None, **kwargs)
await client.issues.search(filter=None, query=None, order=None, expand=None, keys=None, queue=None, per_page=None, page=None)
await client.issues.count(filter=None, query=None)
await client.issues.changelog(issue_id, per_page=None, id=None, field=None, type=None)
await client.issues.move(issue_id, queue, **kwargs)
```

### client.issues.comments

```python
await client.issues.comments.list(issue_id, expand=None)
await client.issues.comments.create(issue_id, text, attachment_ids=None, summonees=None, maillist_summonees=None, markup_type=None)
await client.issues.comments.update(issue_id, comment_id, text, attachment_ids=None, summonees=None, markup_type=None)
await client.issues.comments.delete(issue_id, comment_id)
```

### client.issues.attachments

```python
await client.issues.attachments.list(issue_id)
await client.issues.attachments.attach(issue_id, file_data, filename, new_filename=None)
await client.issues.attachments.upload_temp(file_data, filename, new_filename=None)
await client.issues.attachments.download(issue_id, attachment_id, filename)        # -> bytes
await client.issues.attachments.download_thumbnail(issue_id, attachment_id)        # -> bytes (только изображения)
await client.issues.attachments.delete(issue_id, attachment_id)
```

### client.issues.checklists

```python
await client.issues.checklists.list(issue_id)
await client.issues.checklists.create(issue_id, text, checked=None, assignee=None, deadline=None)
await client.issues.checklists.delete(issue_id)                                   # удаляет ВСЕ пункты
await client.issues.checklists.item.update(issue_id, item_id, text, checked=None, assignee=None, deadline=None)
await client.issues.checklists.item.delete(issue_id, item_id)
```

### client.issues.links

```python
await client.issues.links.list(issue_id)
await client.issues.links.create(issue_id, relationship, linked_issue)
# relationship: 'relates', 'depends on', 'is dependent by', 'is subtask for', 'is parent task for', 'duplicates', 'is duplicated by', 'is epic of', 'has epic'
await client.issues.links.delete(issue_id, link_id)
```

### client.issues.transitions

```python
await client.issues.transitions.list(issue_id)
await client.issues.transitions.update(issue_id, transition_id, comment=None, **fields)
```

### client.issues.bulk

```python
await client.issues.bulk.move(queue, issues, values=None, move_all_fields=None, initial_status=None, notify=None)
await client.issues.bulk.update(issues, values, notify=None)
await client.issues.bulk.transition(transition, issues, values=None, notify=None)
await client.issues.bulk.get_status(bulk_change_id)
await client.issues.bulk.get_failed_issues(bulk_change_id)
```

### client.issues.fields

```python
await client.issues.fields.list()
await client.issues.fields.get(field_id)
await client.issues.fields.create(name, id, category, type, options_provider=None, order=None, description=None, readonly=None, visible=None, hidden=None, container=None)
await client.issues.fields.update(field_id, version, name=None, category=None, order=None, description=None, readonly=None, hidden=None, visible=None, options_provider=None)
await client.issues.fields.create_category(name, order, description=None)
await client.issues.fields.update_category(category_id, version, name=None, order=None, description=None)
```

### client.issues.fields.local

```python
await client.issues.fields.local.list(queue_id)
await client.issues.fields.local.get(queue_id, field_key)
await client.issues.fields.local.create(queue_id, name, id, category, type, options_provider=None, order=None, description=None, readonly=None, visible=None, hidden=None, container=None)
await client.issues.fields.local.update(queue_id, field_key, name=None, category=None, order=None, description=None, options_provider=None, readonly=None, visible=None, hidden=None)
```

### client.issues.types / statuses / resolutions / priorities

```python
await client.issues.types.list()
await client.issues.types.create(key, name)                    # name: {"ru": "...", "en": "..."}
await client.issues.types.update(id_or_key, version=None, name=None)

await client.issues.statuses.list()
await client.issues.statuses.create(key, name, type)           # type: 'new', 'inProgress', 'paused', 'done', 'cancelled'
await client.issues.statuses.update(id_or_key, version=None, name=None, description=None, order=None, type=None)

await client.issues.resolutions.list()
await client.issues.resolutions.create(key, name)
await client.issues.resolutions.update(id_or_key, version=None, name=None, description=None, order=None)

await client.issues.priorities.list(localized=None)
await client.issues.priorities.create(key, name, order, description=None)
await client.issues.priorities.update(id_or_key, version=None, name=None, description=None)
```

### client.entities

`entity_type`: `"project"`, `"portfolio"`, `"goal"`

```python
await client.entities.create(entity_type, summary, lead=None, team_access=None, description=None, markup_type=None, author=None, team_users=None, clients=None, followers=None, start=None, end=None, tags=None, parent_entity=None, entity_status=None, links=None)
await client.entities.get(entity_type, entity_id, fields=None, expand=None)
await client.entities.update(entity_type, entity_id, summary=None, team_access=None, description=None, markup_type=None, author=None, lead=None, team_users=None, clients=None, followers=None, start=None, end=None, tags=None, parent_entity=None, entity_status=None, comment=None, links=None)
await client.entities.delete(entity_type, entity_id, with_board=False)
await client.entities.search(entity_type, fields=None, per_page=None, page=None, input=None, filter=None, order_by=None, order_asc=None, root_only=None)
await client.entities.changelog(entity_type, entity_id, per_page=None, from_event=None, selected=None, new_events_on_top=None, direction=None)
await client.entities.update_key_results(entity_id, key_result_items, comment=None)         # только goal
await client.entities.update_metrics(entity_type, entity_id, metric_items, comment=None)
```

### client.entities.comments

```python
await client.entities.comments.list(entity_type, entity_id, expand=None)
await client.entities.comments.get(entity_type, entity_id, comment_id, expand=None)
await client.entities.comments.create(entity_type, entity_id, text, attachment_ids=None, summonees=None, maillist_summonees=None, is_add_to_followers=None, notify=None, notify_author=None, expand=None)
await client.entities.comments.update(entity_type, entity_id, comment_id, text=None, attachment_ids=None, summonees=None, maillist_summonees=None, is_add_to_followers=None, notify=None, notify_author=None, expand=None)
await client.entities.comments.delete(entity_type, entity_id, comment_id, notify=None, notify_author=None)
```

### client.entities.attachments

```python
await client.entities.attachments.list(entity_type, entity_id)
await client.entities.attachments.get(entity_type, entity_id, file_id)
await client.entities.attachments.attach(entity_type, entity_id, file_id, notify=None, notify_author=None, fields=None, expand=None)
await client.entities.attachments.delete(entity_type, entity_id, file_id)
```

Для прикрепления файла к сущности — двухшаговый процесс:
```python
temp = await client.issues.attachments.upload_temp(file_data=b"...", filename="file.txt")
await client.entities.attachments.attach("project", entity_id, file_id=str(temp["id"]))
```

### client.entities.checklists

```python
await client.entities.checklists.create(entity_type, entity_id, text, checked=None, assignee=None, deadline=None, notify=None, notify_author=None, fields=None, expand=None)
await client.entities.checklists.update(entity_type, entity_id, checklist_items, notify=None, notify_author=None, fields=None, expand=None)
await client.entities.checklists.delete(entity_type, entity_id, ...)                # только project и portfolio
await client.entities.checklists.item.update(entity_type, entity_id, checklist_item_id, text=None, checked=None, assignee=None, deadline=None, ...)
await client.entities.checklists.item.move(entity_type, entity_id, checklist_item_id, before, ...)
await client.entities.checklists.item.delete(entity_type, entity_id, checklist_item_id, ...)
```

### client.entities.links

```python
await client.entities.links.get(entity_type, entity_id, fields=None)
await client.entities.links.create(entity_type, entity_id, relationship, entity)
await client.entities.links.delete(entity_type, entity_id, right)
```

### client.entities.bulk

```python
await client.entities.bulk.update(entity_type, entity_ids, fields=None, comment=None, links=None)
```

### client.entities.settings

```python
await client.entities.settings.get(entity_type, entity_id)
await client.entities.settings.update(entity_type, entity_id, permission_sources=None, acl=None)
```

### client.queues

```python
await client.queues.list(expand=None, per_page=None)
await client.queues.get(queue_id, expand=None)                 # expand: 'projects', 'components', 'versions', 'all'
await client.queues.create(key, name, lead, default_type, default_priority, issue_types_config, description=None, assignee_auto=None, deny_voting=None, deny_conduct_matters=None, use_component_permissions_intersection=None, use_last_signature=None)
await client.queues.delete(queue_id)
await client.queues.restore(queue_id)
```

### client.queues.versions / fields / tags / permissions

```python
await client.queues.versions.list(queue_id)
await client.queues.versions.create(queue, name, description=None, start_date=None, due_date=None)

await client.queues.fields.list(queue_id)

await client.queues.tags.list(queue_id)
await client.queues.tags.delete(queue_id, tag)

await client.queues.permissions.update(queue_id, create=None, write=None, read=None, grant=None)
await client.queues.permissions.get_user(queue_id, user_id)
await client.queues.permissions.get_group(queue_id, group_id)
```

### client.users

```python
await client.users.get_myself(expand=None)
await client.users.get(user_id, expand=None)
await client.users.list(per_page=None, id=None, email=None, group=None, expand=None)
await client.users.get_paginated(per_page=None, id=None, expand=None)
```

### client.boards

```python
await client.boards.list()
await client.boards.list_paginated(per_page=None, id=None)
await client.boards.get(board_id)
await client.boards.create(name, owner=None, board_permissions_template=None, backlog_available=None, sprints_available=None, columns=None, backlog_columns=None, non_parametrized_columns=None, auto_filters=None)
await client.boards.update(board_id, name=None, backlog_available=None, sprints_available=None, columns=None, backlog_columns=None, non_parametrized_columns=None)
await client.boards.delete(board_id)
```

### client.boards.columns / sprints

```python
await client.boards.columns.list(board_id)
await client.boards.columns.get(board_id, column_id)
await client.boards.columns.create(board_id, name, statuses, board_version=None)
await client.boards.columns.update(board_id, column_id, board_version=None, name=None, statuses=None)
await client.boards.columns.delete(board_id, column_id, board_version=None)

await client.boards.sprints.list(board_id)
await client.boards.sprints.get(sprint_id)
await client.boards.sprints.create(name, board_id, start_date, end_date)   # YYYY-MM-DD
```

### client.components

```python
await client.components.list()
await client.components.create(name, queue, description=None, lead=None, assign_auto=None)
await client.components.update(component_id, version=None, name=None, description=None, lead=None, assign_auto=None)
await client.components.permissions.get_user(component_id, user_id)
await client.components.permissions.get_group(component_id, group_id)
```

### client.automations

```python
# Макросы
await client.automations.macros.list(queue)
await client.automations.macros.get(queue, macro_id)
await client.automations.macros.create(queue, name, body=None, issue_update=None)
await client.automations.macros.update(queue, macro_id, name, body=None, issue_update=None)
await client.automations.macros.delete(queue, macro_id)

# Триггеры
await client.automations.triggers.create(queue, name, actions, conditions=None, active=None)
await client.automations.triggers.get(queue, trigger_id)
await client.automations.triggers.update(queue, trigger_id, version=None, name=None, actions=None, conditions=None, active=None)
await client.automations.triggers.get_logs(queue, trigger_id, issue_id=None, limit=None, from_date=None, to_date=None)

# Автодействия
await client.automations.autoactions.create(queue, name, actions, filter=None, query=None, active=None, enable_notifications=None, interval_millis=None, calendar=None)
await client.automations.autoactions.get(queue, autoaction_id)
await client.automations.autoactions.get_logs(queue, autoaction_id, launch_id=None)
```

### client.filters (API v2)

```python
await client.filters.create(name, filter=None, query=None, fields=None, sorts=None, group_by=None, folder=None)
await client.filters.get(filter_id)
await client.filters.update(filter_id, name=None, filter=None, query=None, fields=None, sorts=None, group_by=None, folder=None)
```

### client.dashboards

```python
await client.dashboards.create(name, layout=None, owner=None)
await client.dashboards.create_cycle_time_widget(dashboard_id, description, query=None, filter=None, filter_id=None, from_statuses=None, to_statuses=None, excluded_statuses=None, included_statuses=None, bucket=None, calendar=None, lines=None, start=None, end=None, mode=None, auto_updatable=None)
```

### client.worklog

```python
await client.worklog.create(issue_id, start, duration, comment=None)     # duration: "PT2H30M"
await client.worklog.list(issue_id, per_page=None, id=None)
await client.worklog.search(created_by=None, created_at_from=None, created_at_to=None)
await client.worklog.update(issue_id, worklog_id, duration, comment=None)
await client.worklog.delete(issue_id, worklog_id)
```

### client.imports

```python
await client.imports.issue(queue, summary, created_at, created_by, key=None, updated_at=None, updated_by=None, resolved_at=None, resolved_by=None, resolution=None, status=None, type=None, deadline=None, description=None, start=None, end=None, assignee=None, priority=None, affected_versions=None, fix_versions=None, components=None, tags=None, sprint=None, followers=None, access=None, unique=None, original_estimation=None, estimation=None, spent=None, story_points=None, voted_by=None, favorited_by=None)
await client.imports.comment(issue_id, text, created_at, created_by, updated_at=None, updated_by=None)
await client.imports.link(issue_id, relationship, issue, created_at, created_by, updated_at=None, updated_by=None)
await client.imports.file(issue_id, file_data, filename, created_at, created_by, comment_id=None)
```

### client.external.links

```python
await client.external.links.get_applications()
await client.external.links.list(issue_id)
await client.external.links.create(issue_id, relationship, key, origin, backlink=None)
await client.external.links.delete(issue_id, remotelink_id)
```

---

## Исключения

```python
from YaTrackerApi import TrackerAPIError, BadRequestError, UnauthorizedError, ForbiddenError, NotFoundError, ConflictError, UnprocessableEntityError, LockedError, TooManyRequestsError, ServerError
```

| Класс | HTTP | Когда |
|-------|------|-------|
| `BadRequestError` | 400 | Неверные параметры |
| `UnauthorizedError` | 401 | Невалидный токен |
| `ForbiddenError` | 403 | Нет прав |
| `NotFoundError` | 404 | Объект не найден |
| `ConflictError` | 409 | Конфликт версий |
| `PreconditionFailedError` | 412 | Неактуальная версия (If-Match) |
| `UnprocessableEntityError` | 422 | Ошибка валидации |
| `LockedError` | 423 | Объект заблокирован |
| `PreconditionRequiredError` | 428 | Не передан version |
| `TooManyRequestsError` | 429 | Лимит запросов |
| `ServerError` | 5xx | Ошибка сервера |

Атрибуты: `e.status_code`, `e.url`, `e.method`, `e.error_messages`

---

## Критичные особенности (gotchas)

### 1. snake_case -> camelCase
Все параметры автоматически конвертируются: `per_page` -> `perPage`, `start_date` -> `startDate`.

### 2. entities.search() возвращает dict, не list
```python
result = await client.entities.search(entity_type="project", fields="summary")
projects = result.get("values", [])  # не result напрямую
```

### 3. Параметр fields обязателен для сущностей
Без `fields` API не возвращает большинство полей:
```python
entity = await client.entities.get("project", id, fields="summary,description,lead,teamAccess")
# Данные в entity["fields"]["summary"], не entity["summary"]
```

### 4. type и priority — только ключи
```python
# Неправильно: type=issue["type"]  (полный объект)
# Правильно: type="bug" или type=issue["type"]["key"]
```

### 5. project — только shortId (число)
```python
await client.issues.create(queue="DEV", summary="...", project={"primary": 342})
# НЕ project="68d3c38893e7da46375740b3"
```

### 6. Оптимистичная блокировка (version)
Обновление полей, категорий, компонентов требует `version` из предыдущего ответа. Без него — 428.

### 7. Файлы к сущностям — двухшаговый процесс
Сначала `upload_temp()`, затем `attach()` по `file_id`.

### 8. Чеклисты сущностей — create не возвращает ID пунктов
После создания нужен отдельный GET с `fields="checklistItems"`.

### 9. Удаление чеклиста сущности — только project и portfolio
Для goal удаляйте пункты по одному.

### 10. Фильтры — API v2
Обрабатывается автоматически, но знать полезно при отладке.

### 11. Создание доски — /liveBoards/
`client.boards.create()` использует `/liveBoards/`, не `/boards/`. Обрабатывается автоматически.

### 12. Колонки — If-Match в кавычках
Автоматически. При ручном вызове: `headers = {"If-Match": '"3"'}`.

### 13. Компоненты — кэш get_all
После создания компонента передавайте `version` из ответа create при обновлении.

### 14. Импорт — createdAt в UTC
Используйте единый часовой пояс (`+0000`) для задачи и всех импортируемых данных. Для связей — `createdAt` должен попадать в интервал обеих задач.

### 15. Неудаляемые через API
Задачи (только закрыть), поля (только скрыть), категории полей, очереди (только через веб).

### 16. Теги очереди
`tags.delete()` вернёт 422, если тег используется задачами. Сначала уберите тег со всех задач.

### 17. Системные поля
`createdBy`, `createdAt` нельзя изменить — устанавливаются автоматически.

### 18. Права очереди — формат payload
```python
# Правильно: {право: {тип: {операция: [...]}}}
await client.queues.permissions.update("DEV", create={"users": {"add": ["uid1"]}})
```

### 19. Создание очереди — валидный workflow
В `issue_types_config` нужен реальный ID workflow (например `"W4"`). Получить из существующей очереди через `expand="all"`.

### 20. Debug-логирование
```python
import logging
logging.getLogger("YaTrackerApi").setLevel(logging.DEBUG)
```
