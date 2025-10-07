from typing import List, Dict, Any, Union, Optional
from ..base import BaseAPI

# Типы данных для локальных полей
LocalFieldNameType = Dict[str, str]  # {"en": "English name", "ru": "Русское название"}
LocalFieldTypeType = str  # Тип поля из списка поддерживаемых
LocalCategoryType = str   # ID категории поля
LocalOptionsProviderType = Dict[str, Any]  # Провайдер опций для списков
QueueIdType = Union[str, int]  # ID или ключ очереди

class LocalFieldsAPI(BaseAPI):
    """API для работы с локальными полями задач в очередях"""

    async def get(self, queue_id: QueueIdType, field_key: Optional[str] = None) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Получение локальных полей очереди или конкретного локального поля.

        Args:
            queue_id (QueueIdType): Идентификатор или ключ очереди
            field_key (Optional[str]): Ключ локального поля.
                                     Если не указан, возвращается список всех полей очереди.
                                     Если указан, возвращается информация о конкретном поле.

        Returns:
            Union[List[Dict[str, Any]], Dict[str, Any]]:
                - Список всех локальных полей очереди, если field_key не указан
                - Информацию о конкретном локальном поле, если field_key указан

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если очередь или поле не найдено

        Examples:
            # Получение всех локальных полей очереди
            local_fields = await client.issues.fields.local.get("TESTQUEUE")

            # Получение конкретного локального поля
            field = await client.issues.fields.local.get("TESTQUEUE", "custom_priority_local")

            # Получение по числовому ID очереди
            local_fields = await client.issues.fields.local.get(123)
            field = await client.issues.fields.local.get(123, "custom_field_key")
        """
        # Валидация параметров
        if not isinstance(queue_id, (str, int)):
            raise ValueError("queue_id должен быть строкой или числом")

        if field_key is not None:
            if not isinstance(field_key, str) or not field_key.strip():
                raise ValueError("field_key должен быть непустой строкой")

        if field_key is not None:
            # Получение конкретного локального поля
            self.logger.info(f"Получение локального поля '{field_key}' в очереди {queue_id}")
            endpoint = f'/queues/{queue_id}/localFields/{field_key}'

            result = await self._request(endpoint, 'GET')
            self.logger.info(f"Локальное поле '{field_key}' получено")

            return result
        else:
            # Получение всех локальных полей очереди
            self.logger.info(f"Получение всех локальных полей очереди: {queue_id}")
            endpoint = f'/queues/{queue_id}/localFields'

            result = await self._request(endpoint, 'GET')
            self.logger.info(f"Получено локальных полей для очереди {queue_id}: {len(result)}")

            return result

    async def create(
        self,
        queue_id: QueueIdType,
        name: LocalFieldNameType,
        id: str,
        category: LocalCategoryType,
        type: LocalFieldTypeType,
        options_provider: Optional[LocalOptionsProviderType] = None,
        order: Optional[int] = None,
        description: Optional[str] = None,
        readonly: Optional[bool] = None,
        visible: Optional[bool] = None,
        hidden: Optional[bool] = None,
        container: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Создание нового локального поля задач в очереди.

        Args:
            queue_id (QueueIdType): Идентификатор или ключ очереди
            name (LocalFieldNameType): Название поля на разных языках
                                     {"en": "English", "ru": "Русский"}
            id (str): Идентификатор локального поля
            category (LocalCategoryType): ID категории поля
            type (LocalFieldTypeType): Тип локального поля:
                - ru.yandex.startrek.core.fields.DateFieldType — Дата
                - ru.yandex.startrek.core.fields.DateTimeFieldType — Дата/Время
                - ru.yandex.startrek.core.fields.StringFieldType — Текстовое однострочное
                - ru.yandex.startrek.core.fields.TextFieldType — Текстовое многострочное
                - ru.yandex.startrek.core.fields.FloatFieldType — Дробное число
                - ru.yandex.startrek.core.fields.IntegerFieldType — Целое число
                - ru.yandex.startrek.core.fields.UserFieldType — Имя пользователя
                - ru.yandex.startrek.core.fields.UriFieldType — Ссылка
            options_provider (Optional[LocalOptionsProviderType]): Объект с информацией об элементах списка
            order (Optional[int]): Порядковый номер в списке полей организации
            description (Optional[str]): Описание локального поля
            readonly (Optional[bool]): Возможность редактировать значение поля
                                     (True - только чтение, False - редактируемое)
            visible (Optional[bool]): Признак отображения поля в интерфейсе
                                    (True - всегда отображать, False - не отображать)
            hidden (Optional[bool]): Признак видимости поля в интерфейсе
                                   (True - скрывать поле, False - не скрывать)
            container (Optional[bool]): Возможность указать несколько значений
                                      (True - множественные значения, False - одно значение)

        Returns:
            Dict[str, Any]: Информация о созданном локальном поле

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Examples:
            # Создание простого текстового поля
            local_field = await client.issues.fields.local.create(
                queue_id="TESTQUEUE",
                name={"en": "Custom Priority", "ru": "Кастомный приоритет"},
                id="custom_priority_local",
                category="category_id_here",
                type="ru.yandex.startrek.core.fields.StringFieldType",
                description="Локальное поле для приоритета задач"
            )

            # Создание выпадающего списка
            local_field = await client.issues.fields.local.create(
                queue_id="TESTQUEUE",
                name={"en": "Project Stage", "ru": "Стадия проекта"},
                id="project_stage_local",
                category="category_id_here",
                type="ru.yandex.startrek.core.fields.StringFieldType",
                options_provider={
                    "type": "FixedListOptionsProvider",
                    "values": ["Planning", "Development", "Testing", "Release"]
                },
                visible=True,
                container=False
            )

            # Создание поля пользователя с множественным выбором
            local_field = await client.issues.fields.local.create(
                queue_id="TESTQUEUE",
                name={"en": "Reviewers", "ru": "Ревьюеры"},
                id="reviewers_local",
                category="category_id_here",
                type="ru.yandex.startrek.core.fields.UserFieldType",
                container=True,
                description="Список ревьюеров для задачи"
            )
        """
        # Валидация обязательных параметров
        if not isinstance(queue_id, (str, int)):
            raise ValueError("queue_id должен быть строкой или числом")

        if not isinstance(name, dict) or not name.get('en') or not name.get('ru'):
            raise ValueError("name должен содержать ключи 'en' и 'ru' с непустыми значениями")

        if not isinstance(id, str) or not id.strip():
            raise ValueError("id должен быть непустой строкой")

        if not isinstance(category, str) or not category.strip():
            raise ValueError("category должен быть непустой строкой")

        if not isinstance(type, str) or not type.strip():
            raise ValueError("type должен быть непустой строкой")

        # Проверка типа поля
        valid_types = [
            "ru.yandex.startrek.core.fields.DateFieldType",
            "ru.yandex.startrek.core.fields.DateTimeFieldType",
            "ru.yandex.startrek.core.fields.StringFieldType",
            "ru.yandex.startrek.core.fields.TextFieldType",
            "ru.yandex.startrek.core.fields.FloatFieldType",
            "ru.yandex.startrek.core.fields.IntegerFieldType",
            "ru.yandex.startrek.core.fields.UserFieldType",
            "ru.yandex.startrek.core.fields.UriFieldType"
        ]

        if type not in valid_types:
            raise ValueError(f"type должен быть одним из: {', '.join(valid_types)}")

        self.logger.info(f"Создание локального поля '{name['ru']}' (ID: {id}) в очереди {queue_id}")

        # Формирование payload
        payload = {
            "name": name,
            "id": id,
            "category": category,
            "type": type
        }

        # Добавление опциональных параметров
        if options_provider is not None:
            if not isinstance(options_provider, dict):
                raise ValueError("options_provider должен быть словарем")
            if not options_provider.get('type') or not options_provider.get('values'):
                raise ValueError("options_provider должен содержать ключи 'type' и 'values'")
            payload["optionsProvider"] = options_provider

        if order is not None:
            if not isinstance(order, int):
                raise ValueError("order должен быть числом")
            payload["order"] = order

        if description is not None:
            payload["description"] = str(description)

        if readonly is not None:
            payload["readonly"] = bool(readonly)

        if visible is not None:
            payload["visible"] = bool(visible)

        if hidden is not None:
            payload["hidden"] = bool(hidden)

        if container is not None:
            # Проверка совместимости container с типом поля
            container_compatible_types = [
                "ru.yandex.startrek.core.fields.StringFieldType",
                "ru.yandex.startrek.core.fields.UserFieldType"
            ]
            if type not in container_compatible_types and options_provider is None:
                raise ValueError(f"container=True поддерживается только для типов: {', '.join(container_compatible_types)} или полей с optionsProvider")
            payload["container"] = bool(container)

        self.logger.debug(f"Параметры создания локального поля: {payload}")

        endpoint = f'/queues/{queue_id}/localFields'
        result = await self._request(endpoint, 'POST', data=payload)

        self.logger.info(f"Локальное поле '{name['ru']}' успешно создано с ID: {result.get('id', id)}")

        return result

    async def update(
        self,
        queue_id: QueueIdType,
        field_key: str,
        name: Optional[LocalFieldNameType] = None,
        category: Optional[LocalCategoryType] = None,
        order: Optional[int] = None,
        description: Optional[str] = None,
        options_provider: Optional[LocalOptionsProviderType] = None,
        readonly: Optional[bool] = None,
        visible: Optional[bool] = None,
        hidden: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Обновление локального поля задач в очереди.

        Args:
            queue_id (QueueIdType): Идентификатор или ключ очереди
            field_key (str): Ключ локального поля для обновления
            name (Optional[LocalFieldNameType]): Новое название поля на разных языках
                                               {"en": "English name", "ru": "Русское название"}
            category (Optional[LocalCategoryType]): ID категории поля
            order (Optional[int]): Порядковый номер в списке полей организации
            description (Optional[str]): Описание локального поля
            options_provider (Optional[LocalOptionsProviderType]): Объект с информацией об элементах списка
            readonly (Optional[bool]): Возможность редактировать значение поля
                                     (True - только чтение, False - редактируемое)
            visible (Optional[bool]): Признак отображения поля в интерфейсе
                                    (True - всегда отображать, False - не отображать)
            hidden (Optional[bool]): Признак видимости поля в интерфейсе
                                   (True - скрывать поле, False - не скрывать)

        Returns:
            Dict[str, Any]: Информация об обновленном локальном поле

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если очередь или поле не найдено

        Examples:
            # Обновление только названия локального поля
            updated_field = await client.issues.fields.local.update(
                queue_id="TESTQUEUE",
                field_key="custom_priority_local",
                name={
                    "en": "Updated Custom Priority",
                    "ru": "Обновленный кастомный приоритет"
                }
            )

            # Полное обновление локального поля с опциями
            updated_field = await client.issues.fields.local.update(
                queue_id="TESTQUEUE",
                field_key="project_stage_local",
                name={
                    "en": "Project Stage Updated",
                    "ru": "Обновленная стадия проекта"
                },
                category="new_category_id",
                order=150,
                description="Обновленное описание поля стадии проекта",
                options_provider={
                    "type": "FixedListOptionsProvider",
                    "values": ["Planning", "Development", "Testing", "QA", "Release"]
                },
                readonly=False,
                visible=True,
                hidden=False
            )

            # Обновление настроек отображения
            updated_field = await client.issues.fields.local.update(
                queue_id=123,
                field_key="reviewers_local",
                description="Список ревьюеров с обновленными правами",
                readonly=True,
                visible=False
            )
        """
        # Валидация обязательных параметров
        if not isinstance(queue_id, (str, int)):
            raise ValueError("queue_id должен быть строкой или числом")

        if not isinstance(field_key, str) or not field_key.strip():
            raise ValueError("field_key должен быть непустой строкой")

        # Проверяем, что передан хотя бы один параметр для обновления
        update_params = [name, category, order, description, options_provider, readonly, visible, hidden]
        if all(param is None for param in update_params):
            raise ValueError("Необходимо указать хотя бы один параметр для обновления")

        # Валидация опциональных параметров
        if name is not None:
            if not isinstance(name, dict) or not name.get('en') or not name.get('ru'):
                raise ValueError("name должен содержать ключи 'en' и 'ru' с непустыми значениями")

        if category is not None:
            if not isinstance(category, str) or not category.strip():
                raise ValueError("category должен быть непустой строкой")

        if order is not None:
            if not isinstance(order, int):
                raise ValueError("order должен быть числом")

        if options_provider is not None:
            if not isinstance(options_provider, dict):
                raise ValueError("options_provider должен быть словарем")
            if not options_provider.get('type') or not options_provider.get('values'):
                raise ValueError("options_provider должен содержать ключи 'type' и 'values'")

        self.logger.info(f"Обновление локального поля '{field_key}' в очереди {queue_id}")

        # Формирование payload
        payload = {}

        if name is not None:
            payload["name"] = name

        if category is not None:
            payload["category"] = category

        if order is not None:
            payload["order"] = order

        if description is not None:
            payload["description"] = str(description)

        if options_provider is not None:
            payload["optionsProvider"] = options_provider

        if readonly is not None:
            payload["readonly"] = bool(readonly)

        if visible is not None:
            payload["visible"] = bool(visible)

        if hidden is not None:
            payload["hidden"] = bool(hidden)

        endpoint = f'/queues/{queue_id}/localFields/{field_key}'

        self.logger.debug(f"Параметры обновления локального поля: {payload}")

        result = await self._request(endpoint, 'PATCH', data=payload)

        field_name = name.get('ru', field_key) if name else field_key
        self.logger.info(f"Локальное поле '{field_name}' в очереди {queue_id} успешно обновлено")

        return result