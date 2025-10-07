from typing import List, Dict, Any, Union, Optional
from ..base import BaseAPI
from .local import LocalFieldsAPI

# Типы данных для создания полей
FieldNameType = Dict[str, str]  # {"en": "English name", "ru": "Русское название"}
FieldTypeType = str  # Тип поля из списка поддерживаемых
CategoryType = str   # ID категории поля
OptionsProviderType = Dict[str, Any]  # Провайдер опций для списков

class FieldsAPI(BaseAPI):
    """API для работы с полями задач в Yandex Tracker"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._local = None

    @property
    def local(self) -> LocalFieldsAPI:
        """Доступ к API для работы с локальными полями задач в очередях"""
        if self._local is None:
            self._local = LocalFieldsAPI(self.client)
        return self._local

    async def get(self, field_id: Optional[str] = None) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Получение информации о полях задач.

        Args:
            field_id (Optional[str]): Идентификатор конкретного поля.
                                    Если не указан, возвращает все поля.

        Returns:
            Union[List[Dict[str, Any]], Dict[str, Any]]:
                - Список всех полей, если field_id не указан
                - Информацию об одном поле, если field_id указан

        Raises:
            ValueError: При некорректном field_id
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404 если поле не найдено)

        Examples:
            # Получение всех полей
            all_fields = await client.issues.fields.get()

            # Получение конкретного поля
            field = await client.issues.fields.get('custom_priority_field')
        """
        if field_id is not None:
            # Получение конкретного поля
            if not isinstance(field_id, str) or not field_id.strip():
                raise ValueError("field_id должен быть непустой строкой")

            self.logger.info(f"Получение поля: {field_id}")
            endpoint = f'/fields/{field_id}'

            result = await self._request(endpoint, 'GET')
            self.logger.info(f"Поле '{field_id}' получено")

            return result
        else:
            # Получение всех полей
            self.logger.info(f"Получение всех полей задач")
            endpoint = '/fields'

            result = await self._request(endpoint, 'GET')
            self.logger.info(f"Получено полей: {len(result)}")

            return result

    async def create(
        self,
        name: FieldNameType,
        id: str,
        category: CategoryType,
        type: FieldTypeType,
        options_provider: Optional[OptionsProviderType] = None,
        order: Optional[int] = None,
        description: Optional[str] = None,
        readonly: Optional[bool] = None,
        visible: Optional[bool] = None,
        hidden: Optional[bool] = None,
        container: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Создание нового кастомного поля задач.

        Args:
            name (FieldNameType): Название поля на разных языках {"en": "English", "ru": "Русский"}
            id (str): Идентификатор поля (глобальный ключ)
            category (CategoryType): ID категории поля
            type (FieldTypeType): Тип поля:
                - ru.yandex.startrek.core.fields.DateFieldType — Дата
                - ru.yandex.startrek.core.fields.DateTimeFieldType — Дата/Время
                - ru.yandex.startrek.core.fields.StringFieldType — Текстовое однострочное
                - ru.yandex.startrek.core.fields.TextFieldType — Текстовое многострочное
                - ru.yandex.startrek.core.fields.FloatFieldType — Дробное число
                - ru.yandex.startrek.core.fields.IntegerFieldType — Целое число
                - ru.yandex.startrek.core.fields.UserFieldType — Имя пользователя
                - ru.yandex.startrek.core.fields.UriFieldType — Ссылка
            options_provider (Optional[OptionsProviderType]): Объект с информацией об элементах списка
            order (Optional[int]): Порядковый номер в списке полей организации
            description (Optional[str]): Описание поля
            readonly (Optional[bool]): Возможность редактировать значение (True - только чтение)
            visible (Optional[bool]): Признак отображения поля в интерфейсе
            hidden (Optional[bool]): Признак видимости поля (True - скрывать)
            container (Optional[bool]): Возможность указать несколько значений (как теги)

        Returns:
            Dict[str, Any]: Информация о созданном поле

        Raises:
            ValueError: При некорректных параметрах

        Example:
            # Создание текстового поля
            field = await client.fields.create(
                name={"en": "Custom Priority", "ru": "Кастомный приоритет"},
                id="custom_priority_field",
                category="category_id_here",
                type="ru.yandex.startrek.core.fields.StringFieldType",
                description="Пользовательское поле для приоритета",
                visible=True,
                readonly=False
            )

            # Создание выпадающего списка
            field = await client.fields.create(
                name={"en": "Project Stage", "ru": "Стадия проекта"},
                id="project_stage",
                category="category_id_here",
                type="ru.yandex.startrek.core.fields.StringFieldType",
                options_provider={
                    "type": "FixedListOptionsProvider",
                    "values": ["Planning", "Development", "Testing", "Release"]
                },
                container=False
            )
        """
        # Валидация обязательных параметров
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

        self.logger.info(f"Создание поля '{name['ru']}' (ID: {id})")

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

        self.logger.debug(f"Параметры создания поля: {payload}")

        endpoint = '/fields'
        result = await self._request(endpoint, 'POST', data=payload)

        self.logger.info(f"Поле '{name['ru']}' успешно создано с ID: {result.get('id', id)}")

        return result

    async def update(
        self,
        field_id: str,
        version: str,
        name: Optional[FieldNameType] = None,
        category: Optional[CategoryType] = None,
        order: Optional[int] = None,
        description: Optional[str] = None,
        readonly: Optional[bool] = None,
        hidden: Optional[bool] = None,
        visible: Optional[bool] = None,
        options_provider: Optional[OptionsProviderType] = None
    ) -> Dict[str, Any]:
        """
        Обновление кастомного поля задач.

        Args:
            field_id (str): Идентификатор поля для обновления
            version (str): Текущая версия поля (для оптимистичной блокировки)
            name (Optional[FieldNameType]): Новое название поля на разных языках
                                          {"en": "English name", "ru": "Русское название"}
            category (Optional[CategoryType]): ID категории поля
            order (Optional[int]): Порядковый номер в списке полей организации
            description (Optional[str]): Описание поля
            readonly (Optional[bool]): Возможность редактировать значение поля
                                     (True - только чтение, False - редактируемое)
            hidden (Optional[bool]): Признак видимости поля
                                   (True - скрывать поле, False - не скрывать)
            visible (Optional[bool]): Признак отображения поля в интерфейсе
                                    (True - всегда отображать, False - не отображать)
            options_provider (Optional[OptionsProviderType]): Объект с информацией
                                                            о допустимых значениях поля

        Returns:
            Dict[str, Any]: Информация об обновленном поле

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если поле не найдено
                - 409 если версия поля устарела (конфликт версий)

        Examples:
            # Обновление только названия поля
            updated_field = await client.issues.fields.update(
                field_id="custom_priority_field",
                version="1",
                name={
                    "en": "Updated Priority Field",
                    "ru": "Обновленное поле приоритета"
                }
            )

            # Полное обновление поля с опциями
            updated_field = await client.issues.fields.update(
                field_id="custom_status_field",
                version="2",
                name={
                    "en": "Project Status",
                    "ru": "Статус проекта"
                },
                category="category_id_here",
                order=102,
                description="Поле для отслеживания статуса проекта",
                readonly=False,
                hidden=False,
                visible=True,
                options_provider={
                    "type": "FixedListOptionsProvider",
                    "values": ["Planning", "In Progress", "Testing", "Done"]
                }
            )
        """
        # Валидация обязательных параметров
        if not isinstance(field_id, str) or not field_id.strip():
            raise ValueError("field_id должен быть непустой строкой")

        if not isinstance(version, str) or not version.strip():
            raise ValueError("version должен быть непустой строкой")

        # Проверяем, что передан хотя бы один параметр для обновления
        update_params = [name, category, order, description, readonly, hidden, visible, options_provider]
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

        self.logger.info(f"Обновление поля '{field_id}' (версия: {version})")

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

        if readonly is not None:
            payload["readonly"] = bool(readonly)

        if hidden is not None:
            payload["hidden"] = bool(hidden)

        if visible is not None:
            payload["visible"] = bool(visible)

        if options_provider is not None:
            payload["optionsProvider"] = options_provider

        # Формирование endpoint с параметром version
        endpoint = f'/fields/{field_id}'
        params = {'version': version}

        self.logger.debug(f"Параметры обновления поля: {payload}")

        result = await self._request(endpoint, 'PATCH', data=payload, params=params)

        field_name = name.get('ru', field_id) if name else field_id
        self.logger.info(f"Поле '{field_name}' успешно обновлено")

        return result

    async def create_category(
        self,
        name: FieldNameType,
        order: int,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Создание новой категории полей задач.

        Args:
            name (FieldNameType): Название категории на разных языках
                                {"en": "English name", "ru": "Русское название"}
            order (int): Вес поля при отображении в интерфейсе.
                        Поля с меньшим весом отображаются выше полей с большим весом.
            description (Optional[str]): Описание категории

        Returns:
            Dict[str, Any]: Информация о созданной категории

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Example:
            # Создание категории с описанием
            category = await client.issues.fields.create_category(
                name={
                    "en": "Project Management",
                    "ru": "Управление проектами"
                },
                order=400,
                description="Поля для управления проектами и задачами"
            )

            # Создание простой категории
            category = await client.issues.fields.create_category(
                name={
                    "en": "Custom Fields",
                    "ru": "Пользовательские поля"
                },
                order=500
            )
        """
        # Валидация обязательных параметров
        if not isinstance(name, dict) or not name.get('en') or not name.get('ru'):
            raise ValueError("name должен содержать ключи 'en' и 'ru' с непустыми значениями")

        if not isinstance(order, int):
            raise ValueError("order должен быть числом")

        self.logger.info(f"Создание категории полей '{name['ru']}' (порядок: {order})")

        # Формирование payload
        payload = {
            "name": name,
            "order": order
        }

        # Добавление описания если указано
        if description is not None:
            payload["description"] = str(description)

        self.logger.debug(f"Параметры создания категории: {payload}")

        endpoint = '/fields/categories'
        result = await self._request(endpoint, 'POST', data=payload)

        self.logger.info(f"Категория '{name['ru']}' успешно создана с ID: {result.get('id')}")

        return result