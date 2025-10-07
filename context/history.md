## История изменений

### Базовая функциональность (v0.1-v0.6)
- **v0.1** - Базовый HTTP клиент с OAuth авторизацией
- **v0.2** - Исправление заголовков и SSL конфигурации
- **v0.3** - Система логгирования на русском языке
- **v0.4** - Модульная архитектура + IssuesAPI.get()
- **v0.5** - IssuesAPI.update() + Health Check + удаление legacy кода
- **v0.6** - IssuesAPI.create() + полная поддержка POST операций

### Расширенная функциональность (v0.7-v1.2)
- **v0.7** - Поддержка кастомных полей (localfields) в create() и update()
- **v0.8** - IssuesAPI.move() - перенос задач между очередями
- **v0.9** - Структурированная система примеров examples/
- **v1.0** - IssuesAPI.count() - подсчет задач с фильтрацией
- **v1.1** - IssuesAPI.search() - поиск с сортировкой и пагинацией
- **v1.2** - IssuesAPI.clear_scroll() - управление ресурсами

### Полнофункциональная версия (v1.3-v1.9)
- **v1.3** - IssuesAPI.priorities() - справочная информация о приоритетах
- **v1.4** - TransitionsAPI - управление жизненным циклом задач
- **v1.5** - LinksAPI - управление связями между задачами
- **v1.6** - IssuesAPI.changelog() - история изменений задач
- **v1.7** - ChecklistAPI - управление чеклистами задач
- **v1.8** - FieldsAPI.get() - получение метаданных полей
- **v1.9** - FieldsAPI.create() - создание кастомных полей + **ПУБЛИКАЦИЯ НА PyPI**

### Публикация (2025-01-07)
- **Название пакета**: YaTrackerApi
- **PyPI**: https://pypi.org/project/YaTrackerApi/
- **Установка**: `pip install YaTrackerApi`
- **Лицензия**: MIT
- **Python**: 3.9+
- **Статус**: Production/Stable

### Расширенная версия (v2.0+) - В разработке
- **v2.0** - FieldsAPI.get(field_id) - получение конкретного поля
- **v2.1** - FieldsAPI.update() - обновление кастомных полей с версионированием
- **v2.2** - FieldsAPI.create_category() + LocalFieldsAPI.create() - категории и локальные поля
- **v2.3** - LocalFieldsAPI.get() - получение локальных полей очереди и конкретного поля
- **v2.4** - LocalFieldsAPI.update() - обновление локальных полей в очередях
- **v2.5** - EntitiesAPI.create() - создание сущностей (проекты, портфели, цели)
- **v2.6** - EntitiesAPI.get() - получение информации о сущностях с параметрами
- **v2.7** - EntitiesAPI.update() - обновление сущностей с валидацией статусов
- **v2.8** - EntitiesAPI.delete() - удаление сущностей с параметром withBoard
- **v2.9** - EntitiesAPI.search() - поиск сущностей с фильтрацией, пагинацией и сортировкой
- **v3.0** - EntitiesAPI.bulk_update() - массовое обновление сущностей с валидацией связей
- **v3.1** - EntitiesAPI.changelog() - получение истории изменений сущностей с фильтрацией
- **v3.2** - EntityChecklistsAPI.create() - создание пунктов чеклистов для сущностей
- **v3.3** - Реструктуризация файловой системы: client/<module>/<related_files>.py
- **v3.4** - EntityChecklistsAPI.update() - массовое обновление пунктов чеклистов сущностей
- **v3.5** - EntityChecklistsAPI.update_item() - обновление отдельного пункта чеклиста сущности
- **v3.6** - EntityChecklistsAPI.move_item() - перемещение пункта чеклиста в другую позицию
- **v3.7** - Реструктуризация checklists: добавлен подмодуль item для работы с отдельными пунктами
- **v3.8** - Реструктуризация issues.checklists: добавлен подмодуль item для работы с отдельными пунктами чеклистов задач
- **v3.9** - Реструктуризация entities: добавлен подмодуль bulk для массовых операций (bulk_update() → bulk.update())
- **v3.10** - EntityChecklistsAPI.item.delete() - удаление отдельного пункта чеклиста сущности
- **v3.11** - EntitiesAPI.links.create() - создание связей между сущностями
- **v3.12** - EntitiesAPI.links.get() - получение связей сущности с фильтрацией полей
- **v3.13** - EntitiesAPI.links.delete() - удаление связи между сущностями по параметру right
- **v3.14** - UsersAPI.get() - получение списка всех пользователей организации
- **v3.15** - UsersAPI.get(user_id) - получение информации о конкретном пользователе по логину или ID
- **v3.20** - UsersAPI: объединение методов get() и get_user() в один универсальный метод get()
- **v3.16** - IssuesAPI.comments.create() - создание комментариев к задачам с поддержкой вложений и призывов пользователей
- **v3.17** - IssuesAPI.comments.get() - получение списка комментариев задачи с поддержкой расширенных полей
- **v3.18** - IssuesAPI.comments.update() - обновление существующих комментариев с поддержкой вложений и призывов
- **v3.19** - IssuesAPI.comments.delete() - удаление комментариев с обработкой прав доступа

### Текущий статус
- **Версия**: v2.0.0 (v3.20)
- **Статус**: Полнофункциональный API клиент с управлением всеми сущностями Yandex Tracker
- **Модули**: Issues, Links, Transitions, Checklists, Fields, LocalFields, Entities, Users, Comments
- **Операции**: CRUD + Search + Workflow + References + Integration + Full Fields Management + Entity Management + Comments
- **Breaking Changes в v2.0.0**: Удален метод `get_user()` из UsersAPI, используйте `get(user_id)` вместо него