"""
API модуль для работы с задачами (Issues) в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI
from .links import LinksAPI
from .transitions import TransitionsAPI
from .checklists import ChecklistAPI
from ..fields import FieldsAPI


# Типы для различных полей задачи
QueueType = Union[str, int, Dict[str, Union[str, int]]]  # "TREK", 123 или {"key": "TREK", "id": "123"}
ParentType = Union[str, Dict[str, str]]  # "TASK-123" или {"key": "TASK-123", "id": "123"}
SprintType = Union[int, str, Dict[str, Union[int, str]]]  # 123, "123" или {"id": 123}
TypeType = Union[str, int, Dict[str, Union[str, int]]]  # "bug", 1 или {"key": "bug", "id": "1"}
PriorityType = Union[str, int, Dict[str, Union[str, int]]]  # "minor", 2 или {"key": "minor", "id": "2"}
FollowerType = Union[str, int, Dict[str, Union[str, int]]]  # "userlogin", 123 или {"id": "123"}
AssigneeType = Union[str, int, Dict[str, Union[str, int]]]  # "userlogin", 123 или {"id": "123"}
AuthorType = Union[str, int, Dict[str, Union[str, int]]]  # "userlogin", 123 или {"id": "123"}
LocalFieldsType = Dict[str, Any]  # Кастомные поля пользователя {"customField1": "value1", "priority2025": 100}

# Специальные типы для операций add/remove (только для PATCH)
AddRemoveType = Dict[str, List[str]]  # {"add": ["item1"], "remove": ["item2"]}
ProjectType = Dict[str, Union[int, List[int], AddRemoveType]]  # {"primary": 123, "secondary": [456]} или с add/remove


class IssuesAPI(BaseAPI):
    """API для работы с задачами в Yandex Tracker"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._links = None
        self._transitions = None
        self._checklists = None
        self._fields = None
        self._comments = None
        self._attachments = None
        self._bulk = None
        self._types = None
        self._statuses = None
        self._resolutions = None
        self._priorities = None

    @property
    def links(self) -> LinksAPI:
        """Доступ к API для работы со связями между задачами"""
        if self._links is None:
            self._links = LinksAPI(self.client)
        return self._links

    @property
    def transitions(self) -> TransitionsAPI:
        """Доступ к API для работы с переходами по жизненному циклу задач"""
        if self._transitions is None:
            self._transitions = TransitionsAPI(self.client)
        return self._transitions

    @property
    def checklists(self) -> ChecklistAPI:
        """Доступ к API для работы с чеклистами задач"""
        if self._checklists is None:
            self._checklists = ChecklistAPI(self.client)
        return self._checklists

    @property
    def fields(self) -> FieldsAPI:
        """Доступ к API для работы с полями задач"""
        if self._fields is None:
            self._fields = FieldsAPI(self.client)
        return self._fields

    @property
    def comments(self):
        """Доступ к API для работы с комментариями задач"""
        if self._comments is None:
            from .comments import CommentsAPI
            self._comments = CommentsAPI(self.client)
        return self._comments

    @property
    def attachments(self):
        """Доступ к API для работы с прикреплёнными файлами задач"""
        if self._attachments is None:
            from .attachments import AttachmentsAPI
            self._attachments = AttachmentsAPI(self.client)
        return self._attachments

    @property
    def bulk(self):
        """Доступ к API для пакетных операций с задачами"""
        if self._bulk is None:
            from .bulk import BulkAPI
            self._bulk = BulkAPI(self.client)
        return self._bulk

    @property
    def types(self):
        """Доступ к API для работы с типами задач"""
        if self._types is None:
            from ..issue_types.api import IssueTypesAPI
            self._types = IssueTypesAPI(self.client)
        return self._types

    @property
    def statuses(self):
        """Доступ к API для работы со статусами задач"""
        if self._statuses is None:
            from ..issue_types.api import StatusesAPI
            self._statuses = StatusesAPI(self.client)
        return self._statuses

    @property
    def resolutions(self):
        """Доступ к API для работы с резолюциями"""
        if self._resolutions is None:
            from ..issue_types.api import ResolutionsAPI
            self._resolutions = ResolutionsAPI(self.client)
        return self._resolutions

    @property
    def priorities(self):
        """Доступ к API для работы с приоритетами"""
        if self._priorities is None:
            from ..issue_types.api import PrioritiesAPI
            self._priorities = PrioritiesAPI(self.client)
        return self._priorities

    async def get(self, issue_id: str, expand: Optional[Union[str, List[str]]] = None) -> Dict[str, Any]:
        """
        Получение информации о задаче по ID или ключу
        
        Args:
            issue_id: Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')
            expand: Дополнительные поля для включения в ответ.
                   Может быть строкой или списком строк:
                   - 'transitions' - переходы по жизненному циклу
                   - 'attachments' - вложения
                   Примеры:
                   - expand='attachments'
                   - expand=['transitions', 'attachments']
        
        Returns:
            Dict с информацией о задаче
            
        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404 если задача не найдена)
            
        Examples:
            # Получение базовой информации о задаче
            issue = await client.issues.get('JUNE-3')
            
            # Получение с дополнительными полями
            issue = await client.issues.get('JUNE-3', expand='attachments')
            issue = await client.issues.get('JUNE-3', expand=['transitions', 'attachments'])
        """
        
        # Формируем endpoint
        endpoint = f"/issues/{issue_id}"
        
        # Подготавливаем параметры запроса
        params = {}
        
        if expand:
            # Обрабатываем expand параметр
            if isinstance(expand, str):
                params['expand'] = expand
            elif isinstance(expand, list):
                # Объединяем список в строку через запятую
                params['expand'] = ','.join(expand)
            else:
                self.logger.warning(f"Неподдерживаемый тип для expand: {type(expand)}")
        
        self.logger.debug(f"Получение задачи {issue_id} с параметрами: {params}")
        
        try:
            result = await self._request(endpoint, method='GET', params=params)
            self.logger.info(f"Задача {issue_id} успешно получена")
            return result
            
        except Exception as e:
            self.logger.error(f"Ошибка при получении задачи {issue_id}: {e}")
            raise
    
    async def create(
        self,
        summary: str,
        queue: QueueType,
        # Опциональные параметры
        parent: Optional[ParentType] = None,
        description: Optional[str] = None,
        markup_type: Optional[str] = None,
        sprint: Optional[List[SprintType]] = None,
        issue_type: Optional[TypeType] = None,
        priority: Optional[PriorityType] = None,
        followers: Optional[List[FollowerType]] = None,
        assignee: Optional[AssigneeType] = None,
        author: Optional[AuthorType] = None,
        project: Optional[Dict[str, Union[int, List[int]]]] = None,  # Для создания только primary/secondary без add/remove
        unique: Optional[str] = None,
        attachment_ids: Optional[List[Union[str, int]]] = None,
        description_attachment_ids: Optional[List[Union[str, int]]] = None,
        tags: Optional[List[str]] = None,
        localfields: Optional[LocalFieldsType] = None,  # 🆕 Кастомные поля пользователя
        **kwargs
    ) -> Dict[str, Any]:
        """
        Создание новой задачи (POST запрос)
        
        Args:
            summary: Название задачи (обязательно)
            queue: Очередь для создания задачи (обязательно)
                   Может быть строкой-ключом, числом-id или объектом
            parent: Родительская задача (строка-ключ или объект с id/key)
            description: Описание задачи
            markup_type: Тип разметки в описании ('md' для YFM разметки)
            sprint: Список спринтов для добавления задачи
            issue_type: Тип задачи (объект, строка-ключ или число-id)
            priority: Приоритет задачи (объект, строка-ключ или число-id)
            followers: Список наблюдателей задачи (массив строк/чисел/объектов)
            assignee: Исполнитель задачи (строка-логин, число-id или объект)
            author: Автор задачи (строка-логин, число-id или объект)
            project: Информация о проектах (объект с primary/secondary)
            unique: Уникальное значение для предотвращения дубликатов
            attachment_ids: ID временных файлов для добавления как вложения
            description_attachment_ids: ID временных файлов для описания
            tags: Список тегов задачи
            localfields: Кастомные поля пользователя (словарь ключ-значение)
            **kwargs: Дополнительные поля для создания
            
        Returns:
            Dict с информацией о созданной задаче
            
        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса
            ValueError: При некорректных данных
            
        Examples:
            # Минимальное создание задачи
            issue = await client.issues.create(
                summary="Test Issue",
                queue="TREK"
            )
            
            # Создание с дополнительными параметрами
            issue = await client.issues.create(
                summary="Test Issue",
                queue={"key": "TREK"},
                parent="JUNE-2",
                issue_type="bug",
                assignee="userlogin",
                tags=["тег1", "тег2"]
            )
            
            # Создание с кастомными полями
            issue = await client.issues.create(
                summary="Задача с кастомными полями",
                queue="PROJ",
                description="Подробное описание",
                localfields={
                    "customPriority": "Очень высокий",
                    "businessValue": 85,
                    "estimatedHours": 16.5,
                    "clientName": "ООО Рога и Копыта",
                    "isDraft": False
                }
            )
            
            # Создание с проектами, спринтами и кастомными полями
            issue = await client.issues.create(
                summary="Новая задача",
                queue="PROJ",
                description="Подробное описание",
                markup_type="md",
                sprint=[{"id": "3"}],
                priority={"key": "major"},
                project={
                    "primary": 1234,
                    "secondary": [5678, 9012]
                },
                unique="unique-task-id-2025",
                localfields={
                    "department": "Backend Team",
                    "complexity": 7,
                    "deadline": "2025-12-31"
                }
            )
        """
        
        endpoint = "/issues/"
        
        # Строим payload для POST запроса
        payload = {
            "summary": summary
        }
        
        # Обрабатываем обязательное поле queue
        if isinstance(queue, str):
            payload['queue'] = {"key": queue}
        elif isinstance(queue, int):
            payload['queue'] = {"id": str(queue)}
        elif isinstance(queue, dict):
            payload['queue'] = queue
        else:
            raise ValueError(f"queue должен быть строкой, числом или объектом, получен: {type(queue)}")
        
        # Опциональные поля
        if description is not None:
            payload['description'] = description
            
        if markup_type is not None:
            payload['markupType'] = markup_type
            
        if unique is not None:
            payload['unique'] = unique
        
        # Родительская задача
        if parent is not None:
            if isinstance(parent, str):
                payload['parent'] = {"key": parent}
            elif isinstance(parent, dict):
                payload['parent'] = parent
            else:
                raise ValueError(f"parent должен быть строкой или объектом, получен: {type(parent)}")
        
        # Спринты
        if sprint is not None:
            sprint_list = []
            for s in sprint:
                if isinstance(s, (int, str)):
                    sprint_list.append({"id": str(s)})
                elif isinstance(s, dict):
                    sprint_list.append(s)
                else:
                    raise ValueError(f"sprint элемент должен быть числом, строкой или объектом, получен: {type(s)}")
            payload['sprint'] = sprint_list
        
        # Тип задачи
        if issue_type is not None:
            if isinstance(issue_type, str):
                payload['type'] = {"key": issue_type}
            elif isinstance(issue_type, int):
                payload['type'] = {"id": str(issue_type)}
            elif isinstance(issue_type, dict):
                payload['type'] = issue_type
            else:
                raise ValueError(f"issue_type должен быть строкой, числом или объектом, получен: {type(issue_type)}")
        
        # Приоритет
        if priority is not None:
            if isinstance(priority, str):
                payload['priority'] = {"key": priority}
            elif isinstance(priority, int):
                payload['priority'] = {"id": str(priority)}
            elif isinstance(priority, dict):
                payload['priority'] = priority
            else:
                raise ValueError(f"priority должен быть строкой, числом или объектом, получен: {type(priority)}")
        
        # Исполнитель
        if assignee is not None:
            if isinstance(assignee, str):
                payload['assignee'] = {"login": assignee} if not assignee.isdigit() else {"id": assignee}
            elif isinstance(assignee, int):
                payload['assignee'] = {"id": str(assignee)}
            elif isinstance(assignee, dict):
                payload['assignee'] = assignee
            else:
                raise ValueError(f"assignee должен быть строкой, числом или объектом, получен: {type(assignee)}")
        
        # Автор
        if author is not None:
            if isinstance(author, str):
                payload['author'] = {"login": author} if not author.isdigit() else {"id": author}
            elif isinstance(author, int):
                payload['author'] = {"id": str(author)}
            elif isinstance(author, dict):
                payload['author'] = author
            else:
                raise ValueError(f"author должен быть строкой, числом или объектом, получен: {type(author)}")
        
        # Наблюдатели (для создания - только список, без add/remove)
        if followers is not None:
            if not isinstance(followers, list):
                raise ValueError(f"followers должен быть списком, получен: {type(followers)}")
            
            followers_list = []
            for follower in followers:
                if isinstance(follower, str):
                    followers_list.append({"login": follower} if not follower.isdigit() else {"id": follower})
                elif isinstance(follower, int):
                    followers_list.append({"id": str(follower)})
                elif isinstance(follower, dict):
                    followers_list.append(follower)
                else:
                    raise ValueError(f"follower элемент должен быть строкой, числом или объектом, получен: {type(follower)}")
            payload['followers'] = followers_list
        
        # Проекты (для создания без операций add/remove)
        if project is not None:
            if not isinstance(project, dict):
                raise ValueError(f"project должен быть объектом, получен: {type(project)}")
            payload['project'] = project
        
        # ID вложений
        if attachment_ids is not None:
            # Приводим к строкам
            payload['attachmentIds'] = [str(aid) for aid in attachment_ids]
            
        if description_attachment_ids is not None:
            # Приводим к строкам
            payload['descriptionAttachmentIds'] = [str(aid) for aid in description_attachment_ids]
        
        # Теги (для создания - только список)
        if tags is not None:
            if not isinstance(tags, list):
                raise ValueError(f"tags должен быть списком, получен: {type(tags)}")
            payload['tags'] = tags
        
        # 🆕 Кастомные поля пользователя
        if localfields is not None:
            if not isinstance(localfields, dict):
                raise ValueError(f"localfields должен быть словарем, получен: {type(localfields)}")
            
            self.logger.debug(f"Добавление кастомных полей: {list(localfields.keys())}")
            
            # Добавляем каждое кастомное поле напрямую в payload
            for field_key, field_value in localfields.items():
                if field_key in payload:
                    self.logger.warning(f"Кастомное поле '{field_key}' перезаписывает стандартное поле")
                payload[field_key] = field_value
        
        # Дополнительные поля из kwargs
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = value
        
        self.logger.info(f"Создание новой задачи в очереди {queue}")
        self.logger.debug(f"Поля для создания: {list(payload.keys())}")
        
        try:
            result = await self._request(endpoint, method='POST', data=payload)
            created_key = result.get('key', 'неизвестный')
            self.logger.info(f"Задача {created_key} успешно создана")
            return result
            
        except Exception as e:
            self.logger.error(f"Ошибка при создании задачи: {e}")
            raise
    
    async def update(
        self, 
        issue_id: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        parent: Optional[ParentType] = None,
        markup_type: Optional[str] = None,
        sprint: Optional[List[SprintType]] = None,
        issue_type: Optional[TypeType] = None,
        priority: Optional[PriorityType] = None,
        followers: Optional[Union[List[FollowerType], AddRemoveType]] = None,
        project: Optional[ProjectType] = None,
        attachment_ids: Optional[List[str]] = None,
        description_attachment_ids: Optional[List[str]] = None,
        tags: Optional[Union[List[str], AddRemoveType]] = None,
        localfields: Optional[LocalFieldsType] = None,  # 🆕 Кастомные поля пользователя
        **kwargs
    ) -> Dict[str, Any]:
        """
        Обновление задачи (PATCH запрос)
        
        Args:
            issue_id: Идентификатор или ключ задачи для обновления
            summary: Новое название задачи
            description: Новое описание задачи
            parent: Родительская задача (строка-ключ или объект с id/key)
            markup_type: Тип разметки в описании ('md' для YFM разметки)
            sprint: Список спринтов для добавления задачи
            issue_type: Новый тип задачи (объект, строка-ключ или число-id)
            priority: Новый приоритет задачи (объект, строка-ключ или число-id)
            followers: Наблюдатели задачи (список или объект с add/remove)
            project: Информация о проектах (объект с primary/secondary)
            attachment_ids: ID временных файлов для добавления как вложения
            description_attachment_ids: ID временных файлов для описания
            tags: Теги задачи (список или объект с add/remove)
            localfields: Кастомные поля пользователя (словарь ключ-значение)
            **kwargs: Дополнительные поля для обновления
            
        Returns:
            Dict с обновленной информацией о задаче
            
        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса
            ValueError: При некорректных данных
            
        Examples:
            # Пример 1: Изменить название, описание, тип и приоритет
            await client.issues.update(
                'TEST-1',
                summary="Новое название задачи",
                description="Новое описание задачи",
                issue_type={"id": "1", "key": "bug"},
                priority={"id": "2", "key": "minor"}
            )
            
            # Пример 2: Изменить родителя, добавить в спринты, добавить наблюдателей
            await client.issues.update(
                'TEST-1',
                parent={"key": "TEST-2"},
                sprint=[{"id": "3"}, {"id": "2"}],
                followers={"add": ["userlogin-1", "userlogin-2"]}
            )
            
            # Пример 3: Операции с тегами и кастомными полями
            await client.issues.update(
                'TEST-1',
                tags={"add": ["тег1"], "remove": ["тег2"]},
                localfields={
                    "customPriority": "Критический",
                    "estimatedHours": 24,
                    "clientFeedback": "Требует срочного исправления"
                }
            )
            
            # Пример 4: Изменить проекты и обновить кастомные поля
            await client.issues.update(
                'TEST-1',
                project={
                    "primary": 1234,
                    "secondary": {"add": [5678]}
                },
                localfields={
                    "department": "Frontend Team",  # Обновить отдел
                    "complexity": 9,                 # Повысить сложность
                    "reviewRequired": True           # Добавить флаг проверки
                }
            )
        """
        
        endpoint = f"/issues/{issue_id}"
        
        # Строим payload для PATCH запроса
        payload = {}
        
        # Простые строковые поля
        if summary is not None:
            payload['summary'] = summary
            
        if description is not None:
            payload['description'] = description
            
        if markup_type is not None:
            payload['markupType'] = markup_type
            
        # Родительская задача
        if parent is not None:
            if isinstance(parent, str):
                payload['parent'] = {"key": parent}
            elif isinstance(parent, dict):
                payload['parent'] = parent
            else:
                raise ValueError(f"parent должен быть строкой или объектом, получен: {type(parent)}")
        
        # Спринты
        if sprint is not None:
            sprint_list = []
            for s in sprint:
                if isinstance(s, (int, str)):
                    sprint_list.append({"id": str(s)})
                elif isinstance(s, dict):
                    sprint_list.append(s)
                else:
                    raise ValueError(f"sprint элемент должен быть числом, строкой или объектом, получен: {type(s)}")
            payload['sprint'] = sprint_list
        
        # Тип задачи
        if issue_type is not None:
            if isinstance(issue_type, str):
                payload['type'] = {"key": issue_type}
            elif isinstance(issue_type, int):
                payload['type'] = {"id": str(issue_type)}
            elif isinstance(issue_type, dict):
                payload['type'] = issue_type
            else:
                raise ValueError(f"issue_type должен быть строкой, числом или объектом, получен: {type(issue_type)}")
        
        # Приоритет
        if priority is not None:
            if isinstance(priority, str):
                payload['priority'] = {"key": priority}
            elif isinstance(priority, int):
                payload['priority'] = {"id": str(priority)}
            elif isinstance(priority, dict):
                payload['priority'] = priority
            else:
                raise ValueError(f"priority должен быть строкой, числом или объектом, получен: {type(priority)}")
        
        # Наблюдатели
        if followers is not None:
            if isinstance(followers, list):
                # Простой список наблюдателей (замена)
                payload['followers'] = followers
            elif isinstance(followers, dict) and ('add' in followers or 'remove' in followers):
                # Операции add/remove
                payload['followers'] = followers
            else:
                raise ValueError(f"followers должен быть списком или объектом с add/remove, получен: {type(followers)}")
        
        # Проекты
        if project is not None:
            if not isinstance(project, dict):
                raise ValueError(f"project должен быть объектом, получен: {type(project)}")
            payload['project'] = project
        
        # ID вложений
        if attachment_ids is not None:
            payload['attachmentIds'] = attachment_ids
            
        if description_attachment_ids is not None:
            payload['descriptionAttachmentIds'] = description_attachment_ids
        
        # Теги
        if tags is not None:
            if isinstance(tags, list):
                # Простой список тегов (замена)
                payload['tags'] = tags
            elif isinstance(tags, dict) and ('add' in tags or 'remove' in tags):
                # Операции add/remove
                payload['tags'] = tags
            else:
                raise ValueError(f"tags должен быть списком или объектом с add/remove, получен: {type(tags)}")
        
        # 🆕 Кастомные поля пользователя
        if localfields is not None:
            if not isinstance(localfields, dict):
                raise ValueError(f"localfields должен быть словарем, получен: {type(localfields)}")
            
            self.logger.debug(f"Обновление кастомных полей: {list(localfields.keys())}")
            
            # Добавляем каждое кастомное поле напрямую в payload
            for field_key, field_value in localfields.items():
                if field_key in payload:
                    self.logger.warning(f"Кастомное поле '{field_key}' перезаписывает стандартное поле")
                payload[field_key] = field_value
        
        # Дополнительные поля из kwargs
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = value
        
        # Проверяем что есть что обновлять
        if not payload:
            raise ValueError("Не указано ни одного поля для обновления")
        
        self.logger.info(f"Обновление задачи {issue_id}")
        self.logger.debug(f"Поля для обновления: {list(payload.keys())}")
        
        try:
            result = await self._request(endpoint, method='PATCH', data=payload)
            self.logger.info(f"Задача {issue_id} успешно обновлена")
            return result
            
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении задачи {issue_id}: {e}")
            raise
    
    async def move(
        self,
        issue_id: str,
        queue: str,
        notify: Optional[bool] = None,
        notify_author: Optional[bool] = None,
        move_all_fields: Optional[bool] = None,
        initial_status: Optional[bool] = None,
        expand: Optional[Union[str, List[str]]] = None
    ) -> Dict[str, Any]:
        """
        Перенос задачи в другую очередь
        
        Args:
            issue_id: Идентификатор или ключ задачи для переноса
            queue: Ключ очереди, в которую необходимо перенести задачу (обязательно)
            notify: Признак уведомления пользователей об изменении задачи:
                   - True (по умолчанию): пользователи получат уведомления
                   - False: пользователи не получат уведомления
            notify_author: Признак уведомления автора задачи:
                          - True: автор получит уведомление
                          - False (по умолчанию): автор не получит уведомление
            move_all_fields: Перенос версий, компонентов и проектов в новую очередь:
                           - True: перенести, если в новой очереди существуют соответствующие объекты
                           - False (по умолчанию): очистить версии, компоненты, проекты
            initial_status: Сброс статуса задачи в начальное значение:
                          - True: статус будет сброшен в начальное значение новой очереди
                          - False (по умолчанию): статус останется без изменений
            expand: Дополнительные поля для включения в ответ.
                   Может быть строкой или списком строк:
                   - 'attachments': вложения
                   - 'comments': комментарии
                   - 'workflow': рабочий процесс задачи
                   - 'transitions': переходы по жизненному циклу
                   Примеры:
                   - expand='attachments'
                   - expand=['transitions', 'attachments']
        
        Returns:
            Dict с обновленной информацией о перенесенной задаче
            
        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса
            ValueError: При некорректных данных
            
        Examples:
            # Простой перенос задачи в другую очередь
            result = await client.issues.move('TEST-123', 'NEWQUEUE')
            
            # Перенос с уведомлениями автора и пользователей
            result = await client.issues.move(
                'TEST-123', 
                'NEWQUEUE',
                notify=True,
                notify_author=True
            )
            
            # Перенос с переносом всех полей и сбросом статуса
            result = await client.issues.move(
                'TEST-123',
                'NEWQUEUE', 
                move_all_fields=True,
                initial_status=True,
                expand=['transitions', 'attachments']
            )
            
            # Тихий перенос без уведомлений с получением дополнительной информации
            result = await client.issues.move(
                'PROJ-456',
                'ARCHIVE',
                notify=False,
                expand=['workflow', 'comments']
            )
        """
        
        # Валидация обязательных параметров
        if not queue or not isinstance(queue, str):
            raise ValueError(f"queue должен быть непустой строкой, получен: {queue}")
        
        # Формируем endpoint
        endpoint = f"/issues/{issue_id}/_move"
        
        # Подготавливаем параметры запроса
        params = {
            'queue': queue
        }
        
        # Добавляем опциональные булевы параметры
        if notify is not None:
            params['notify'] = str(notify).lower()  # Конвертируем в 'true'/'false'
            
        if notify_author is not None:
            params['notifyAuthor'] = str(notify_author).lower()
            
        if move_all_fields is not None:
            params['moveAllFields'] = str(move_all_fields).lower()
            
        if initial_status is not None:
            params['initialStatus'] = str(initial_status).lower()
        
        # Обрабатываем expand параметр (аналогично методу get())
        if expand:
            if isinstance(expand, str):
                params['expand'] = expand
            elif isinstance(expand, list):
                # Объединяем список в строку через запятую
                params['expand'] = ','.join(expand)
            else:
                self.logger.warning(f"Неподдерживаемый тип для expand: {type(expand)}")
        
        self.logger.info(f"Перенос задачи {issue_id} в очередь {queue}")
        self.logger.debug(f"Параметры переноса: {params}")
        
        try:
            result = await self._request(endpoint, method='POST', params=params)
            moved_key = result.get('key', issue_id)
            self.logger.info(f"Задача {moved_key} успешно перенесена в очередь {queue}")
            return result
            
        except Exception as e:
            self.logger.error(f"Ошибка при переносе задачи {issue_id} в очередь {queue}: {e}")
            raise
    
    # Заготовки для будущих методов
    async def delete(self, issue_id: str) -> Dict[str, Any]:
        """
        Удаление задачи
        
        Args:
            issue_id: Идентификатор или ключ задачи
            
        Returns:
            Dict с результатом удаления
            
        Note:
            Метод будет реализован в следующих итерациях
        """
        raise NotImplementedError("Метод delete будет реализован позже")
    
    async def count(
        self,
        filter: Optional[Dict[str, Any]] = None,
        query: Optional[str] = None
    ) -> int:
        """
        Подсчет количества задач с указанными параметрами фильтрации

        Args:
            filter: Объект с парами "поле": "значение" для фильтрации задач.
                   Можно использовать любые поля задач, включая:
                   - queue: очередь (строка или объект)
                   - assignee: исполнитель ("login" или "empty()")
                   - status: статус задачи
                   - priority: приоритет
                   - author: автор задачи
                   - tags: теги задачи
                   - created: дата создания
                   Пример: {"queue": "JUNE", "assignee": "empty()"}

            query: Фильтр на языке запросов Yandex Tracker.
                  Альтернативный способ фильтрации с более гибким синтаксисом.
                  Пример: "Queue: JUNE AND Assignee: empty()"

        Returns:
            int: Количество задач, соответствующих критериям фильтрации

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса
            ValueError: Если не указан ни filter, ни query

        Examples:
            # Подсчет задач без исполнителя в очереди JUNE
            count = await client.issues.count(filter={
                "queue": "JUNE",
                "assignee": "empty()"
            })

            # Подсчет задач по нескольким критериям
            count = await client.issues.count(filter={
                "queue": "PROJ",
                "status": "open",
                "priority": "major"
            })

            # Использование языка запросов
            count = await client.issues.count(
                query="Queue: JUNE AND Status: Open AND Priority: Major"
            )

            # Подсчет задач с кастомными полями
            count = await client.issues.count(filter={
                "queue": "TECH",
                "customPriority": "Высокий"
            })
        """

        # Проверяем, что указан хотя бы один параметр фильтрации
        if filter is None and query is None:
            raise ValueError("Необходимо указать filter или query для подсчета задач")

        # Подготавливаем payload для POST запроса
        payload = {}

        if filter is not None:
            if not isinstance(filter, dict):
                raise ValueError("filter должен быть словарем")
            payload["filter"] = filter
            self.logger.debug(f"Добавлен фильтр: {filter}")

        if query is not None:
            if not isinstance(query, str):
                raise ValueError("query должен быть строкой")
            payload["query"] = query
            self.logger.debug(f"Добавлен запрос: {query}")

        endpoint = "/issues/_count"

        self.logger.info(f"Выполнение подсчета задач")
        self.logger.debug(f"Параметры подсчета: {payload}")

        try:
            result = await self._request(endpoint, method='POST', data=payload)

            # API возвращает просто число, а не объект
            if isinstance(result, int):
                count = result
            elif isinstance(result, dict) and 'count' in result:
                # На случай, если API изменится в будущем
                count = result['count']
            else:
                # Пытаемся преобразовать к числу
                try:
                    count = int(result)
                except (ValueError, TypeError):
                    self.logger.warning(f"Неожиданный тип ответа: {type(result)}, значение: {result}")
                    count = 0

            self.logger.info(f"Подсчет задач завершен: найдено {count} задач")
            return count

        except Exception as e:
            self.logger.error(f"Ошибка при подсчете задач: {e}")
            raise

    async def search(
        self,
        queue: Optional[str] = None,
        keys: Optional[Union[str, List[str]]] = None,
        filter: Optional[Dict[str, Any]] = None,
        query: Optional[str] = None,
        order: Optional[str] = None,
        expand: Optional[Union[str, List[str]]] = None,
        per_page: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Поиск задач с расширенными возможностями фильтрации и сортировки

        Args:
            queue: Очередь для поиска задач (например, "TREK", "PROJ")
            keys: Ключи конкретных задач для получения.
                 Может быть строкой ("TASK-123") или списком (["TASK-123", "TASK-124"])
            filter: Объект с парами "поле": "значение" для фильтрации задач.
                   Можно использовать любые поля задач, включая:
                   - queue: очередь
                   - assignee: исполнитель
                   - status: статус задачи
                   - priority: приоритет
                   - author: автор задачи
                   - tags: теги задачи
                   - created: дата создания
            query: Фильтр на языке запросов Yandex Tracker с сортировкой.
                  Пример: "Queue: TREK AND Status: Open \"Sort by\": Updated DESC"
            order: Направление и поле сортировки (только с filter).
                  Формат: "+поле" (возрастание) или "-поле" (убывание)
                  Примеры: "+status", "-created", "+priority"
            expand: Дополнительные поля для включения в ответ:
                   - 'transitions' - переходы по жизненному циклу
                   - 'attachments' - вложения
                   Может быть строкой или списком строк
            per_page: Количество задач на странице (по умолчанию 50)

        Returns:
            List[Dict]: Список задач, соответствующих критериям поиска

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса
            ValueError: При некорректных параметрах или их комбинациях

        Note:
            Приоритеты параметров (в порядке убывания):
            1. queue - наивысший приоритет
            2. keys
            3. filter
            4. query - наименьший приоритет

            Нельзя использовать более 2 параметров одновременно.

        Examples:
            # Поиск всех задач в очереди
            tasks = await client.issues.search(queue="TREK")

            # Поиск конкретных задач по ключам
            tasks = await client.issues.search(keys=["TASK-123", "TASK-124"])

            # Поиск с фильтрацией и сортировкой
            tasks = await client.issues.search(
                filter={"queue": "TREK", "assignee": "empty()"},
                order="+status",
                expand=["transitions", "attachments"],
                per_page=100
            )

            # Поиск с помощью языка запросов
            tasks = await client.issues.search(
                query="Queue: TREK AND Status: Open \"Sort by\": Updated DESC",
                expand="attachments"
            )

            # Поиск задач с кастомными полями
            tasks = await client.issues.search(filter={
                "queue": "TECH",
                "customPriority": "Высокий"
            })
        """

        # Подготавливаем параметры и payload
        params = {}
        payload = {}

        # Подсчитываем количество основных параметров поиска
        search_params = [queue, keys, filter, query]
        active_params = [p for p in search_params if p is not None]

        if len(active_params) == 0:
            raise ValueError("Необходимо указать один из параметров: queue, keys, filter или query")

        if len(active_params) > 2:
            raise ValueError("Можно использовать максимум 2 параметра одновременно")

        # Обрабатываем основные параметры поиска по приоритету
        if queue is not None:
            if not isinstance(queue, str):
                raise ValueError("queue должен быть строкой")
            payload["queue"] = queue
            self.logger.debug(f"Добавлен параметр queue: {queue}")

        elif keys is not None:
            if isinstance(keys, str):
                payload["keys"] = keys
            elif isinstance(keys, list):
                if not all(isinstance(key, str) for key in keys):
                    raise ValueError("Все элементы keys должны быть строками")
                payload["keys"] = keys
            else:
                raise ValueError("keys должен быть строкой или списком строк")
            self.logger.debug(f"Добавлен параметр keys: {keys}")

        elif filter is not None:
            if not isinstance(filter, dict):
                raise ValueError("filter должен быть словарем")
            payload["filter"] = filter
            self.logger.debug(f"Добавлен параметр filter: {filter}")

        elif query is not None:
            if not isinstance(query, str):
                raise ValueError("query должен быть строкой")
            payload["query"] = query
            self.logger.debug(f"Добавлен параметр query: {query}")

        # Обрабатываем дополнительные параметры
        if order is not None:
            if filter is None:
                raise ValueError("order можно использовать только совместно с filter")
            if not isinstance(order, str):
                raise ValueError("order должен быть строкой")
            if not (order.startswith('+') or order.startswith('-')):
                raise ValueError("order должен начинаться с '+' или '-' (например, '+status' или '-created')")
            payload["order"] = order
            self.logger.debug(f"Добавлен параметр order: {order}")

        # Обрабатываем expand параметр
        if expand is not None:
            if isinstance(expand, str):
                params['expand'] = expand
            elif isinstance(expand, list):
                if not all(isinstance(item, str) for item in expand):
                    raise ValueError("Все элементы expand должны быть строками")
                params['expand'] = ','.join(expand)
            else:
                raise ValueError("expand должен быть строкой или списком строк")
            self.logger.debug(f"Добавлен параметр expand: {expand}")

        # Обрабатываем per_page параметр
        if per_page is not None:
            if not isinstance(per_page, int) or per_page <= 0:
                raise ValueError("per_page должен быть положительным числом")
            params['perPage'] = per_page
            self.logger.debug(f"Добавлен параметр per_page: {per_page}")

        endpoint = "/issues/_search"

        self.logger.info(f"Выполнение поиска задач")
        self.logger.debug(f"Параметры поиска: {payload}")
        self.logger.debug(f"Параметры запроса: {params}")

        try:
            result = await self._request(endpoint, method='POST', data=payload, params=params)

            # API возвращает список задач
            if isinstance(result, list):
                tasks = result
            else:
                # На случай, если API изменится и будет возвращать объект
                tasks = result.get('issues', [])

            self.logger.info(f"Поиск задач завершен: найдено {len(tasks)} задач")
            return tasks

        except Exception as e:
            self.logger.error(f"Ошибка при поиске задач: {e}")
            raise

    async def clear_scroll(self, scroll_sessions: Dict[str, str]) -> Dict[str, Any]:
        """
        Очистка скролл-сессий после поиска задач

        Используется для освобождения серверных ресурсов после завершения работы
        с постраничными результатами поиска, полученными через search().

        Args:
            scroll_sessions: Словарь с парами "scrollId": "scrollToken".
                           scrollId и scrollToken получаются из заголовков
                           X-Scroll-Id и X-Scroll-Token при поиске задач.
                           Количество пар равно количеству страниц результатов.

        Returns:
            Dict: Ответ от API об успешной очистке сессий

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса
            ValueError: При некорректных параметрах

        Examples:
            # После получения результатов поиска с заголовками скролла
            scroll_sessions = {
                "cXVlcnlUaGVuRmV0Y2g...": "c44356850f446b88e5b5cd65a34a1409...",
                "cXVlcnlUaGVuRmV0Y2c...": "b8e1c56966f037d9c4e241af40d31dc8..."
            }

            # Очистка скролл-сессий
            result = await client.issues.clear_scroll(scroll_sessions)

            # Обычно используется в паре с search() при работе с большими объемами данных:
            # 1. Выполняется поиск задач
            # 2. Обрабатываются результаты по страницам
            # 3. Очищаются скролл-сессии для освобождения ресурсов

        Note:
            Этот метод следует вызывать после завершения работы с постраничными
            результатами поиска для освобождения серверных ресурсов.
        """

        if not scroll_sessions:
            raise ValueError("scroll_sessions не может быть пустым")

        if not isinstance(scroll_sessions, dict):
            raise ValueError("scroll_sessions должен быть словарем")

        # Проверяем, что все ключи и значения являются строками
        for scroll_id, scroll_token in scroll_sessions.items():
            if not isinstance(scroll_id, str) or not isinstance(scroll_token, str):
                raise ValueError("Все ключи и значения в scroll_sessions должны быть строками")

        endpoint = "/system/search/scroll/_clear"

        self.logger.info(f"Очистка скролл-сессий: {len(scroll_sessions)} сессий")
        self.logger.debug(f"Очищаемые сессии: {list(scroll_sessions.keys())}")

        try:
            result = await self._request(endpoint, method='POST', data=scroll_sessions)

            self.logger.info(f"Скролл-сессии успешно очищены")
            return result

        except Exception as e:
            self.logger.error(f"Ошибка при очистке скролл-сессий: {e}")
            raise

    async def changelog(
        self,
        issue_id: str,
        id: Optional[str] = None,
        per_page: Optional[int] = None,
        field: Optional[str] = None,
        type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Получение истории изменений задачи

        Возвращает список всех изменений задачи в хронологическом порядке.
        Поддерживает пагинацию и фильтрацию по полям и типам изменений.

        Args:
            issue_id: Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')
            id: Идентификатор изменения, с которого начинать возврат результатов
            per_page: Количество изменений на странице (по умолчанию 50, максимум 100)
            field: Идентификатор поля для фильтрации изменений
                  (например, 'status', 'assignee', 'checklists', 'description')
            type: Тип изменения для фильтрации ('IssueUpdated', 'IssueCreated', 'IssueCommented')

        Returns:
            List[Dict]: Список изменений с подробной информацией о каждом изменении

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404, 400, 403)
            ValueError: При некорректных параметрах

        Examples:
            # Получение всех изменений задачи
            changelog = await client.issues.changelog('TASK-123')

            # Анализ изменений
            for change in changelog:
                author = change.get('updatedBy', {}).get('display', 'System')
                updated_at = change.get('updatedAt', 'Unknown')
                print(f"Изменение от {author} в {updated_at}")

                # Просмотр конкретных изменений полей
                for field_change in change.get('fields', []):
                    field_name = field_change.get('field', {}).get('display', 'Unknown')
                    from_value = field_change.get('from', {}).get('display', 'None')
                    to_value = field_change.get('to', {}).get('display', 'None')
                    print(f"  {field_name}: {from_value} -> {to_value}")

            # Получение изменений с пагинацией
            changelog_page = await client.issues.changelog('TASK-123', per_page=20)

            # Фильтрация по полю статуса
            status_changes = await client.issues.changelog(
                'TASK-123',
                field='status'
            )

            # Фильтрация по типу изменения
            updates_only = await client.issues.changelog(
                'TASK-123',
                type='IssueUpdated'
            )

            # Получение изменений чеклиста
            checklist_changes = await client.issues.changelog(
                'TASK-123',
                field='checklists'
            )

            # Комбинированная фильтрация
            assignee_updates = await client.issues.changelog(
                'TASK-123',
                field='assignee',
                type='IssueUpdated',
                per_page=10
            )

            # Получение изменений начиная с определенного ID
            changelog_from_id = await client.issues.changelog(
                'TASK-123',
                id='change_id_123'
            )

            # Анализ активности задачи
            total_changes = len(changelog)
            authors = set(change.get('updatedBy', {}).get('login') for change in changelog)
            print(f"Всего изменений: {total_changes}, участников: {len(authors)}")

            # Группировка изменений по дням
            from collections import defaultdict
            changes_by_date = defaultdict(list)
            for change in changelog:
                date = change.get('updatedAt', '')[:10]  # YYYY-MM-DD
                changes_by_date[date].append(change)

            # Результат содержит полную историю задачи
            print(f"Получено {len(changelog)} изменений для задачи {issue_id}")
        """

        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        if per_page is not None and (not isinstance(per_page, int) or per_page <= 0 or per_page > 100):
            raise ValueError("per_page должен быть положительным числом не больше 100")

        if id is not None and not isinstance(id, str):
            raise ValueError("id должен быть строкой")

        if field is not None and not isinstance(field, str):
            raise ValueError("field должен быть строкой")

        if type is not None and not isinstance(type, str):
            raise ValueError("type должен быть строкой")

        endpoint = f"/issues/{issue_id}/changelog"

        # Подготавливаем параметры запроса
        params = {}

        if id is not None:
            params['id'] = id

        if per_page is not None:
            params['perPage'] = per_page

        if field is not None:
            params['field'] = field

        if type is not None:
            params['type'] = type

        self.logger.info(f"Получение истории изменений для задачи: {issue_id}")

        if params:
            param_info = []
            if id:
                param_info.append(f"с ID: {id}")
            if per_page:
                param_info.append(f"лимит: {per_page}")
            if field:
                param_info.append(f"поле: {field}")
            if type:
                param_info.append(f"тип: {type}")

            self.logger.debug(f"Параметры фильтрации: {', '.join(param_info)}")

        try:
            result = await self._request(endpoint, method='GET', params=params)

            # Проверяем, что получили список
            if not isinstance(result, list):
                self.logger.warning(f"Неожиданный тип ответа: {type(result)}")
                result = []

            changes_count = len(result)
            self.logger.info(f"Получено {changes_count} изменений для задачи {issue_id}")

            if changes_count > 0:
                # Анализируем изменения для логирования
                authors = set()
                field_types = set()
                change_types = set()

                for change in result:
                    # Собираем статистику по авторам
                    author = change.get('updatedBy', {}).get('login')
                    if author:
                        authors.add(author)

                    # Собираем статистику по типам изменений
                    change_type = change.get('type')
                    if change_type:
                        change_types.add(change_type)

                    # Собираем статистику по измененным полям
                    for field_change in change.get('fields', []):
                        field_name = field_change.get('field', {}).get('key')
                        if field_name:
                            field_types.add(field_name)

                self.logger.debug(f"Уникальных авторов: {len(authors)}")
                if field_types:
                    self.logger.debug(f"Измененные поля: {', '.join(sorted(field_types))}")
                if change_types:
                    self.logger.debug(f"Типы изменений: {', '.join(sorted(change_types))}")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при получении истории изменений для задачи {issue_id}: {e}")
            raise

    async def suggest(
        self,
        input: str,
        queue: Optional[str] = None,
        full: Optional[bool] = None,
        fields: Optional[Union[str, List[str]]] = None,
        expand: Optional[Union[str, List[str]]] = None,
        embed: Optional[Union[str, List[str]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Формирование подсказок (suggest) при поиске задач.

        Возвращает список задач, в названии которых содержится указанный
        фрагмент текста. В ответ попадут только те задачи, к которым у
        пользователя есть доступ.

        Args:
            input (str): Фрагмент текста для поиска задач. Если между словами
                        указан пробел, в выдачу также попадут результаты,
                        в которых есть любой текст на месте пробела.
            queue (Optional[str]): Ключ очереди, в которой будет выполнен поиск.
            full (Optional[bool]): Вывести подробную информацию о каждой задаче.
                                  Значение по умолчанию — False.
                                  Обязательный параметр для включения fields, expand, embed.
            fields (Optional[Union[str, List[str]]]): Поля задачи для включения в ответ.
                                                     Например: "summary,status,assignee"
                                                     или ["summary", "status", "assignee"].
                                                     Требуется full=True.
            expand (Optional[Union[str, List[str]]]): Дополнительная информация в ответе.
                                                     Доступные значения: all, html, attachments,
                                                     comments, links, localLinkRefs, aliases,
                                                     transitions, permissions, sla, update_limits.
                                                     Требуется full=True.
            embed (Optional[Union[str, List[str]]]): Подробная информация о параметрах из expand.
                                                    Доступные значения: attachments, comments,
                                                    transitions, sla.
                                                    Требуется full=True.

        Returns:
            List[Dict[str, Any]]: Список найденных задач

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Examples:
            # Простой поиск по тексту
            issues = await client.issues.suggest(input="исправить ошибки")

            # Поиск в конкретной очереди
            issues = await client.issues.suggest(
                input="баг авторизации",
                queue="TESTBOT"
            )

            # Поиск с подробной информацией
            issues = await client.issues.suggest(
                input="исправить ошибки",
                full=True,
                fields=["summary", "status", "assignee", "followers"]
            )

            # Поиск с расширенными полями
            issues = await client.issues.suggest(
                input="релиз",
                full=True,
                fields="summary,status",
                expand="transitions",
                embed="transitions"
            )
        """
        # Валидация обязательных параметров
        if not isinstance(input, str) or not input.strip():
            raise ValueError("input должен быть непустой строкой")

        if queue is not None and (not isinstance(queue, str) or not queue.strip()):
            raise ValueError("queue должен быть непустой строкой")

        if full is not None and not isinstance(full, bool):
            raise ValueError("full должен быть boolean")

        # Предупреждение: fields/expand/embed требуют full=True
        if (fields is not None or expand is not None or embed is not None) and not full:
            self.logger.warning("Параметры fields, expand, embed требуют full=True для работы")

        self.logger.info(f"Формирование подсказок по запросу: '{input}'")

        # Формирование параметров запроса
        params = {'input': input}

        if queue is not None:
            params['queue'] = queue

        if full is not None:
            params['full'] = str(full).lower()

        if fields is not None:
            if isinstance(fields, list):
                params['fields'] = ','.join(fields)
            else:
                params['fields'] = fields

        if expand is not None:
            if isinstance(expand, list):
                params['expand'] = ','.join(expand)
            else:
                params['expand'] = expand

        if embed is not None:
            if isinstance(embed, list):
                params['embed'] = ','.join(embed)
            else:
                params['embed'] = embed

        self.logger.debug(f"Параметры suggest-запроса: {params}")

        endpoint = '/issues/_suggest'

        try:
            result = await self._request(endpoint, method='GET', params=params)

            issues_count = len(result) if isinstance(result, list) else 0
            self.logger.info(f"Найдено {issues_count} задач по подсказке '{input}'")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при формировании подсказок по запросу '{input}': {e}")
            raise

    async def report(
        self,
        summary: str,
        format: str = 'xlsx',
        query: Optional[str] = None,
        filter: Optional[Dict[str, Any]] = None,
        filter_id: Optional[int] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        report_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Создание отчета по задачам.

        Формирует отчет (экспорт) по задачам в формате xlsx, xml или csv.
        Для фильтрации задач можно использовать один из параметров: query, filter или filter_id.

        Args:
            summary (str): Название отчета
            format (str): Формат выгрузки. Допустимые значения: "xlsx", "xml", "csv".
                          По умолчанию "xlsx".
            query (Optional[str]): Фильтр на языке запросов Yandex Tracker.
                                  Например: 'Queue: SUPPORT "Sort by": Updated DESC'
            filter (Optional[Dict[str, Any]]): Параметры фильтрации задач.
                                              Можно указать название любого поля и значение.
                                              Например: {"queue": "TESTBOT", "assignee": "empty()"}
            filter_id (Optional[int]): Идентификатор сохраненного фильтра.
            sorts (Optional[List[Dict[str, Any]]]): Массив объектов с параметрами сортировки.
                                                   Каждый объект: {"orderBy": "field", "orderAsc": bool}
            report_fields (Optional[List[str]]): Список полей задачи для включения в отчет.
                                                Например: ["priority", "type", "key", "summary",
                                                "assignee", "status", "updated"]

        Returns:
            Dict[str, Any]: Информация о созданном отчете

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Examples:
            # Отчет с языком запросов
            report = await client.issues.report(
                summary="Выгрузка задач SUPPORT",
                format="xlsx",
                query='Queue: SUPPORT "Sort by": Updated DESC',
                sorts=[{"orderBy": "updated", "orderAsc": False}],
                report_fields=["priority", "type", "key", "summary", "assignee", "status", "updated"]
            )

            # Отчет с фильтром по полям
            report = await client.issues.report(
                summary="Задачи без исполнителя",
                format="csv",
                filter={"queue": "TREK", "assignee": "empty()"},
                report_fields=["key", "summary", "status"]
            )

            # Отчет по сохраненному фильтру
            report = await client.issues.report(
                summary="Отчет по фильтру",
                format="xml",
                filter_id=12345
            )
        """
        # Валидация обязательных параметров
        if not isinstance(summary, str) or not summary.strip():
            raise ValueError("summary должен быть непустой строкой")

        valid_formats = ['xlsx', 'xml', 'csv']
        if format not in valid_formats:
            raise ValueError(f"format должен быть одним из: {', '.join(valid_formats)}")

        # Проверяем, что указан только один из параметров фильтрации
        filter_params = [p for p in [query, filter, filter_id] if p is not None]
        if len(filter_params) > 1:
            raise ValueError("Можно использовать только один из параметров: query, filter, filter_id")

        if sorts is not None:
            if not isinstance(sorts, list):
                raise ValueError("sorts должен быть списком объектов")
            for sort in sorts:
                if not isinstance(sort, dict) or 'orderBy' not in sort:
                    raise ValueError("Каждый объект в sorts должен содержать ключ 'orderBy'")

        if report_fields is not None:
            if not isinstance(report_fields, list):
                raise ValueError("report_fields должен быть списком строк")

        if filter_id is not None and not isinstance(filter_id, int):
            raise ValueError("filter_id должен быть числом")

        self.logger.info(f"Создание отчета '{summary}' в формате {format}")

        # Формирование объекта filter для API
        filter_obj = {}

        if query is not None:
            filter_obj['query'] = query

        if filter is not None:
            filter_obj['filter'] = filter

        if filter_id is not None:
            filter_obj['filterId'] = filter_id

        if sorts is not None:
            filter_obj['sorts'] = sorts

        # Формирование объекта parameters
        parameters = {
            'type': 'issueFilterExport',
            'format': format,
            'filter': filter_obj
        }

        if report_fields is not None:
            parameters['fields'] = report_fields

        # Формирование payload
        payload = {
            'fields': {
                'summary': summary,
                'parameters': parameters
            }
        }

        self.logger.debug(f"Параметры создания отчета: {payload}")

        endpoint = '/entities/report/'

        try:
            result = await self._request(endpoint, method='POST', data=payload)

            report_id = result.get('id', 'N/A')
            self.logger.info(f"Отчет '{summary}' успешно создан с ID: {report_id}")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при создании отчета '{summary}': {e}")
            raise

    async def list(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Получение списка задач с фильтрацией

        Args:
            **kwargs: Параметры фильтрации (queue, assignee, status и др.)

        Returns:
            List[Dict] со списком задач

        Note:
            Метод будет реализован в следующих итерациях.
            Используйте метод search() для поиска задач.
        """
        raise NotImplementedError("Метод list будет реализован позже. Используйте search() вместо list().")
