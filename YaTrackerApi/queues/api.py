"""
API модуль для работы с очередями (Queues) в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


# Типы для различных полей очереди
LeadType = Union[str, int, Dict[str, Union[str, int]]]  # "userlogin", 123 или {"id": "123"}
IssueTypeType = Union[str, int, Dict[str, Union[str, int]]]  # "bug", 1 или {"key": "bug"}
PriorityType = Union[str, int, Dict[str, Union[str, int]]]  # "normal", 2 или {"key": "normal"}


class QueuesAPI(BaseAPI):
    """API для работы с очередями в Yandex Tracker"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._versions = None
        self._fields = None
        self._tags = None
        self._bulk = None
        self._user = None
        self._group = None

    @property
    def versions(self):
        """Доступ к API для работы с версиями очереди"""
        if self._versions is None:
            from .versions import VersionsAPI
            self._versions = VersionsAPI(self.client)
        return self._versions

    @property
    def fields(self):
        """Доступ к API для работы с полями очереди"""
        if self._fields is None:
            from .fields import FieldsAPI
            self._fields = FieldsAPI(self.client)
        return self._fields

    @property
    def tags(self):
        """Доступ к API для работы с тегами очереди"""
        if self._tags is None:
            from .tags import TagsAPI
            self._tags = TagsAPI(self.client)
        return self._tags

    @property
    def bulk(self):
        """Доступ к API для массового управления доступом к очереди"""
        if self._bulk is None:
            from .bulk import BulkAPI
            self._bulk = BulkAPI(self.client)
        return self._bulk

    @property
    def user(self):
        """Доступ к API для получения доступа пользователя к очереди"""
        if self._user is None:
            from .user import UserAPI
            self._user = UserAPI(self.client)
        return self._user

    @property
    def group(self):
        """Доступ к API для получения доступа группы к очереди"""
        if self._group is None:
            from .group import GroupAPI
            self._group = GroupAPI(self.client)
        return self._group

    async def get(
        self,
        queue_id: Optional[str] = None,
        expand: Optional[Union[str, List[str]]] = None,
        per_page: Optional[int] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Получение информации об очереди или списке очередей

        Args:
            queue_id: Идентификатор или ключ очереди (например, 'TREK').
                     Если не указан, возвращает список всех очередей.
            expand: Дополнительные поля для включения в ответ.
                   Может быть строкой или списком строк:
                   - 'projects' - проекты очереди
                   - 'components' - компоненты очереди
                   - 'versions' - версии очереди
                   - 'all' - все дополнительные поля
                   Примеры:
                   - expand='projects'
                   - expand=['projects', 'components']
            per_page: Количество очередей на странице (только для списка очередей, по умолчанию 50)

        Returns:
            Dict с информацией об очереди или List[Dict] со списком очередей

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404 если очередь не найдена)

        Examples:
            # Получение списка всех очередей
            queues = await client.queues.get()

            # Получение информации о конкретной очереди
            queue = await client.queues.get('TREK')

            # Получение с дополнительными полями
            queue = await client.queues.get('TREK', expand='all')
        """

        # Подготавливаем параметры запроса
        params = {}

        if expand:
            # Обрабатываем expand параметр
            if isinstance(expand, str):
                params['expand'] = expand
            elif isinstance(expand, list):
                params['expand'] = ','.join(expand)
            else:
                self.logger.warning(f"Неподдерживаемый тип для expand: {type(expand)}")

        if per_page is not None and queue_id is None:
            params['perPage'] = per_page

        # Формируем endpoint
        if queue_id:
            endpoint = f"/queues/{queue_id}"
            self.logger.debug(f"Получение очереди {queue_id} с параметрами: {params}")
        else:
            endpoint = "/queues/"
            self.logger.debug(f"Получение списка очередей с параметрами: {params}")

        try:
            result = await self._request(endpoint, method='GET', params=params if params else None)
            if queue_id:
                self.logger.info(f"Очередь {queue_id} успешно получена")
            else:
                self.logger.info(f"Список очередей успешно получен")
            return result

        except Exception as e:
            if queue_id:
                self.logger.error(f"Ошибка при получении очереди {queue_id}: {e}")
            else:
                self.logger.error(f"Ошибка при получении списка очередей: {e}")
            raise

    async def create(
        self,
        key: str,
        name: str,
        lead: LeadType,
        default_type: IssueTypeType,
        default_priority: PriorityType,
        issue_types_config: List[Dict[str, Any]],
        # Опциональные параметры
        description: Optional[str] = None,
        assignee_auto: Optional[bool] = None,
        deny_voting: Optional[bool] = None,
        deny_conduct_matters: Optional[bool] = None,
        use_component_permissions_intersection: Optional[bool] = None,
        use_last_signature: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Создание новой очереди

        Args:
            key: Ключ очереди (идентификатор)
            name: Название очереди
            lead: Владелец очереди (логин пользователя, ID или объект)
            default_type: Тип задачи по умолчанию (ключ типа, ID или объект)
            default_priority: Приоритет по умолчанию (ключ приоритета, ID или объект)
            issue_types_config: Конфигурация типов задач
                Список объектов с полями:
                - issueType: тип задачи
                - workflow: ID или ключ workflow
                - resolutions: список возможных резолюций
            description: Описание очереди
            assignee_auto: Автоматическое назначение исполнителя
            deny_voting: Запретить голосование
            deny_conduct_matters: Запретить ведение дел
            use_component_permissions_intersection: Использовать пересечение прав компонентов
            use_last_signature: Использовать последнюю подпись

        Returns:
            Dict с информацией о созданной очереди

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса
            ValueError: При некорректных параметрах

        Examples:
            # Создание простой очереди
            queue = await client.queues.create(
                key='DESIGN',
                name='Design',
                lead='username',
                default_type='task',
                default_priority='normal',
                issue_types_config=[
                    {
                        'issueType': 'task',
                        'workflow': 'oicn',
                        'resolutions': ['wontFix']
                    }
                ]
            )
        """

        endpoint = "/queues/"

        # Формируем payload
        payload = {
            'key': key,
            'name': name,
            'issueTypesConfig': issue_types_config
        }

        # Обрабатываем lead
        if isinstance(lead, str):
            payload['lead'] = lead
        elif isinstance(lead, int):
            payload['lead'] = str(lead)
        elif isinstance(lead, dict):
            payload['lead'] = lead
        else:
            raise ValueError(f"lead должен быть строкой, числом или объектом")

        # Обрабатываем default_type
        if isinstance(default_type, str):
            payload['defaultType'] = default_type
        elif isinstance(default_type, int):
            payload['defaultType'] = {'id': str(default_type)}
        elif isinstance(default_type, dict):
            payload['defaultType'] = default_type
        else:
            raise ValueError(f"default_type должен быть строкой, числом или объектом")

        # Обрабатываем default_priority
        if isinstance(default_priority, str):
            payload['defaultPriority'] = default_priority
        elif isinstance(default_priority, int):
            payload['defaultPriority'] = {'id': str(default_priority)}
        elif isinstance(default_priority, dict):
            payload['defaultPriority'] = default_priority
        else:
            raise ValueError(f"default_priority должен быть строкой, числом или объектом")

        # Добавляем опциональные параметры
        if description is not None:
            payload['description'] = description
        if assignee_auto is not None:
            payload['assigneeAutoAssign'] = assignee_auto
        if deny_voting is not None:
            payload['denyVoting'] = deny_voting
        if deny_conduct_matters is not None:
            payload['denyConductMatters'] = deny_conduct_matters
        if use_component_permissions_intersection is not None:
            payload['useComponentPermissionsIntersection'] = use_component_permissions_intersection
        if use_last_signature is not None:
            payload['useLastSignature'] = use_last_signature

        self.logger.debug(f"Создание очереди с ключом {key}")

        try:
            result = await self._request(endpoint, method='POST', data=payload)
            self.logger.info(f"Очередь {key} успешно создана")
            return result

        except Exception as e:
            self.logger.error(f"Ошибка при создании очереди {key}: {e}")
            raise

    async def delete(self, queue_id: str) -> None:
        """
        Удаление очереди

        Args:
            queue_id: Идентификатор или ключ очереди

        Returns:
            None (при успешном удалении возвращается статус 204)

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Examples:
            # Удаление очереди
            await client.queues.delete('TREK')
        """

        endpoint = f"/queues/{queue_id}"

        self.logger.debug(f"Удаление очереди {queue_id}")

        try:
            await self._request(endpoint, method='DELETE')
            self.logger.info(f"Очередь {queue_id} успешно удалена")

        except Exception as e:
            self.logger.error(f"Ошибка при удалении очереди {queue_id}: {e}")
            raise

    async def restore(self, queue_id: str) -> Dict[str, Any]:
        """
        Восстановление удаленной очереди

        Args:
            queue_id: Идентификатор или ключ очереди

        Returns:
            Dict с информацией о восстановленной очереди

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404 если очередь не может быть восстановлена)

        Examples:
            # Восстановление удаленной очереди
            queue = await client.queues.restore('TREK')
        """

        endpoint = f"/queues/{queue_id}/_restore"

        self.logger.debug(f"Восстановление очереди {queue_id}")

        try:
            result = await self._request(endpoint, method='POST')
            self.logger.info(f"Очередь {queue_id} успешно восстановлена")
            return result

        except Exception as e:
            self.logger.error(f"Ошибка при восстановлении очереди {queue_id}: {e}")
            raise
