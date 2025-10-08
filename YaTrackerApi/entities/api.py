from typing import List, Dict, Any, Union, Optional
from ..base import BaseAPI

# Типы данных для сущностей
EntityType = str  # Тип сущности: project, portfolio, goal
EntityFieldsType = Dict[str, Any]  # Поля сущности
ParentEntityType = Dict[str, Union[str, List[str]]]  # Родительские сущности
EntityLinkType = Dict[str, str]  # Связь с другой сущностью

class EntitiesAPI(BaseAPI):
    """API для работы с сущностями (проекты, портфели, цели) в Yandex Tracker"""

    @property
    def checklists(self):
        """API для работы с чеклистами сущностей"""
        if not hasattr(self, '_checklists'):
            from .checklists import EntityChecklistsAPI
            self._checklists = EntityChecklistsAPI(self.client)
        return self._checklists

    @property
    def bulk(self):
        """API для массовых операций с сущностями"""
        if not hasattr(self, '_bulk'):
            from .bulk import BulkAPI
            self._bulk = BulkAPI(self.client)
        return self._bulk

    @property
    def links(self):
        """API для работы со связями сущностей"""
        if not hasattr(self, '_links'):
            from .links import LinksAPI
            self._links = LinksAPI(self.client)
        return self._links

    async def create(
        self,
        entity_type: EntityType,
        summary: str,
        lead: Optional[str] = None,
        team_access: Optional[bool] = None,
        description: Optional[str] = None,
        markup_type: Optional[str] = None,
        author: Optional[str] = None,
        team_users: Optional[List[str]] = None,
        clients: Optional[List[str]] = None,
        followers: Optional[List[str]] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        tags: Optional[List[str]] = None,
        parent_entity: Optional[ParentEntityType] = None,
        entity_status: Optional[str] = None,
        links: Optional[List[EntityLinkType]] = None
    ) -> Dict[str, Any]:
        """
        Создание новой сущности (проект, портфель, цель).

        Args:
            entity_type (EntityType): Тип создаваемой сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            summary (str): Название сущности (обязательное поле)
            lead (Optional[str]): Ответственный (идентификатор пользователя)
            team_access (Optional[bool]): Настройки доступа
                                   - True: доступ только для участников проекта/портфеля/цели
                                   - False: доступ имеют другие пользователи
            description (Optional[str]): Описание сущности
            markup_type (Optional[str]): Тип разметки (например, "md" для YFM)
            author (Optional[str]): Автор (идентификатор пользователя)
            team_users (Optional[List[str]]): Участники (массив идентификаторов пользователей)
            clients (Optional[List[str]]): Заказчики (массив идентификаторов пользователей)
            followers (Optional[List[str]]): Наблюдатели (массив идентификаторов пользователей)
            start (Optional[str]): Дата начала в формате YYYY-MM-DDThh:mm:ss.sss±hhmm
            end (Optional[str]): Дедлайн в формате YYYY-MM-DDThh:mm:ss.sss±hhmm
            tags (Optional[List[str]]): Теги
            parent_entity (Optional[ParentEntityType]): Данные о родительских сущностях
                                                      {"primary": "parent_id", "secondary": ["additional_ids"]}
            entity_status (Optional[str]): Статус сущности
            links (Optional[List[EntityLinkType]]): Связи с другими сущностями
                                                  [{"relationship": "depends on", "entity": "entity_id"}]

        Returns:
            Dict[str, Any]: Информация о созданной сущности

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Examples:
            # Создание простого проекта
            project = await client.issues.entities.create(
                entity_type="project",
                summary="Новый проект",
                lead="username",
                description="Описание проекта"
            )

            # Создание портфеля с участниками и дедлайном
            portfolio = await client.issues.entities.create(
                entity_type="portfolio",
                summary="Портфель проектов 2025",
                lead="manager",
                description="Стратегический портфель на 2025 год",
                team_users=["user1", "user2", "user3"],
                clients=["client1", "client2"],
                followers=["observer1"],
                start="2025-01-01T00:00:00.000+0300",
                end="2025-12-31T23:59:59.000+0300",
                tags=["strategic", "2025"],
                team_access=True
            )

            # Создание цели с родительской сущностью и связями
            goal = await client.issues.entities.create(
                entity_type="goal",
                summary="Увеличить конверсию на 20%",
                lead="product_manager",
                description="Цель по увеличению конверсии в Q1",
                parent_entity={"primary": "parent_goal_id"},
                entity_status="in_progress",
                links=[
                    {"relationship": "is supported by", "entity": "support_project_id"}
                ],
                end="2025-03-31T23:59:59.000+0300"
            )
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(summary, str) or not summary.strip():
            raise ValueError("summary должен быть непустой строкой")

        # Валидация опциональных параметров
        if lead is not None and (not isinstance(lead, str) or not lead.strip()):
            raise ValueError("lead должен быть непустой строкой")

        if team_access is not None and not isinstance(team_access, bool):
            raise ValueError("team_access должен быть boolean")

        if markup_type is not None and not isinstance(markup_type, str):
            raise ValueError("markup_type должен быть строкой")

        if team_users is not None and not isinstance(team_users, list):
            raise ValueError("team_users должен быть списком строк")

        if clients is not None and not isinstance(clients, list):
            raise ValueError("clients должен быть списком строк")

        if followers is not None and not isinstance(followers, list):
            raise ValueError("followers должен быть списком строк")

        if tags is not None and not isinstance(tags, list):
            raise ValueError("tags должен быть списком строк")

        if parent_entity is not None:
            if not isinstance(parent_entity, dict):
                raise ValueError("parent_entity должен быть словарем")
            if "primary" not in parent_entity:
                raise ValueError("parent_entity должен содержать ключ 'primary'")

        if links is not None:
            if not isinstance(links, list):
                raise ValueError("links должен быть списком словарей")
            for link in links:
                if not isinstance(link, dict) or "relationship" not in link or "entity" not in link:
                    raise ValueError("каждая связь должна содержать ключи 'relationship' и 'entity'")

        self.logger.info(f"Создание сущности типа '{entity_type}': {summary}")

        # Формирование полей сущности
        fields = {
            "summary": summary
        }

        # Добавление опциональных полей
        if lead is not None:
            fields["lead"] = lead

        if team_access is not None:
            fields["teamAccess"] = team_access

        if description is not None:
            fields["description"] = description

        if markup_type is not None:
            fields["markupType"] = markup_type

        if author is not None:
            fields["author"] = author

        if team_users is not None:
            fields["teamUsers"] = team_users

        if clients is not None:
            fields["clients"] = clients

        if followers is not None:
            fields["followers"] = followers

        if start is not None:
            fields["start"] = start

        if end is not None:
            fields["end"] = end

        if tags is not None:
            fields["tags"] = tags

        if parent_entity is not None:
            fields["parentEntity"] = parent_entity

        if entity_status is not None:
            fields["entityStatus"] = entity_status

        # Формирование payload
        payload = {"fields": fields}

        if links is not None:
            payload["links"] = links

        self.logger.debug(f"Параметры создания сущности: {payload}")

        endpoint = f'/entities/{entity_type}'
        result = await self._request(endpoint, 'POST', data=payload)

        self.logger.info(f"Сущность '{entity_type}' '{summary}' успешно создана с ID: {result.get('id')}")

        return result

    async def get(
        self,
        entity_type: EntityType,
        entity_id: str,
        fields: Optional[str] = None,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Получение информации о сущности (проект, портфель, цель).

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_id (str): Идентификатор сущности (id или shortId)
            fields (Optional[str]): Дополнительные поля сущности для включения в ответ
                                  Например: "summary,teamAccess,description,tags"
            expand (Optional[str]): Дополнительная информация для включения в ответ
                                  - "attachments" - вложенные файлы

        Returns:
            Dict[str, Any]: Информация о сущности

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если сущность не найдена

        Examples:
            # Получение базовой информации о проекте
            project = await client.entities.get("project", "PROJECT-123")

            # Получение портфеля с дополнительными полями
            portfolio = await client.entities.get(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                fields="summary,teamAccess,description,tags"
            )

            # Получение цели с вложениями
            goal = await client.entities.get(
                entity_type="goal",
                entity_id="GOAL-789",
                expand="attachments"
            )

            # Получение проекта со всеми дополнительными данными
            project = await client.entities.get(
                entity_type="project",
                entity_id="PROJECT-123",
                fields="summary,teamAccess,description,tags,start,end,lead,status",
                expand="attachments"
            )
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        # Валидация опциональных параметров
        if fields is not None and not isinstance(fields, str):
            raise ValueError("fields должен быть строкой")

        if expand is not None and not isinstance(expand, str):
            raise ValueError("expand должен быть строкой")

        self.logger.info(f"Получение сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}'

        # Формирование параметров запроса
        params = {}

        if fields is not None:
            params['fields'] = fields

        if expand is not None:
            params['expand'] = expand

        self.logger.debug(f"Параметры запроса сущности: {params}")

        result = await self._request(endpoint, 'GET', params=params)

        self.logger.info(f"Сущность {entity_type} '{entity_id}' успешно получена")

        return result

    async def update(
        self,
        entity_type: EntityType,
        entity_id: str,
        summary: Optional[str] = None,
        team_access: Optional[bool] = None,
        description: Optional[str] = None,
        markup_type: Optional[str] = None,
        author: Optional[str] = None,
        lead: Optional[str] = None,
        team_users: Optional[List[str]] = None,
        clients: Optional[List[str]] = None,
        followers: Optional[List[str]] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        tags: Optional[List[str]] = None,
        parent_entity: Optional[ParentEntityType] = None,
        entity_status: Optional[str] = None,
        comment: Optional[str] = None,
        links: Optional[List[EntityLinkType]] = None
    ) -> Dict[str, Any]:
        """
        Обновление сущности (проект, портфель, цель).

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_id (str): Идентификатор сущности (id или shortId)
            summary (Optional[str]): Новое название сущности
            team_access (Optional[bool]): Настройки доступа
                                        - True: доступ только для участников
                                        - False: доступ имеют другие пользователи
            description (Optional[str]): Описание сущности
            markup_type (Optional[str]): Тип разметки (например, "md" для YFM)
            author (Optional[str]): Автор (идентификатор пользователя)
            lead (Optional[str]): Ответственный (идентификатор пользователя)
            team_users (Optional[List[str]]): Участники (массив идентификаторов пользователей)
            clients (Optional[List[str]]): Заказчики (массив идентификаторов пользователей)
            followers (Optional[List[str]]): Наблюдатели (массив идентификаторов пользователей)
            start (Optional[str]): Дата начала в формате YYYY-MM-DDThh:mm:ss.sss±hhmm
            end (Optional[str]): Дедлайн в формате YYYY-MM-DDThh:mm:ss.sss±hhmm
            tags (Optional[List[str]]): Теги
            parent_entity (Optional[ParentEntityType]): Данные о родительских сущностях
                                                      {"primary": "parent_id", "secondary": ["additional_ids"]}
            entity_status (Optional[str]): Статус сущности
                                          Для проектов: draft, draft2, in_progress, according_to_plan,
                                          postponed, at_risk, blocked, launched, cancelled
                                          Для целей: draft, according_to_plan, at_risk, blocked,
                                          achieved, partially_achieved, not_achieved, exceeded, cancelled
            comment (Optional[str]): Комментарий к изменению
            links (Optional[List[EntityLinkType]]): Связи с другими сущностями
                                                  [{"relationship": "depends on", "entity": "entity_id"}]

        Returns:
            Dict[str, Any]: Информация об обновленной сущности

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если сущность не найдена

        Examples:
            # Простое обновление названия проекта
            project = await client.entities.update(
                entity_type="project",
                entity_id="PROJECT-123",
                summary="Обновленное название проекта"
            )

            # Полное обновление портфеля
            portfolio = await client.entities.update(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                summary="Новое название портфеля",
                description="Обновленное описание",
                team_access=True,
                lead="new_manager",
                team_users=["user1", "user2", "user3"],
                clients=["client1"],
                end="2025-12-31T23:59:59.000+0300",
                tags=["updated", "strategic"],
                entity_status="in_progress",
                comment="Обновление параметров портфеля"
            )

            # Обновление цели с родительской сущностью и связями
            goal = await client.entities.update(
                entity_type="goal",
                entity_id="GOAL-789",
                summary="Увеличить конверсию на 25%",
                description="Пересмотренная цель по конверсии",
                parent_entity={"primary": "new_parent_goal_id"},
                entity_status="according_to_plan",
                links=[
                    {"relationship": "is supported by", "entity": "support_project_id"},
                    {"relationship": "depends on", "entity": "dependency_goal_id"}
                ],
                comment="Корректировка цели по итогам Q1"
            )
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        # Проверяем, что передан хотя бы один параметр для обновления
        update_params = [
            summary, team_access, description, markup_type, author, lead,
            team_users, clients, followers, start, end, tags,
            parent_entity, entity_status, comment, links
        ]
        if all(param is None for param in update_params):
            raise ValueError("Необходимо указать хотя бы один параметр для обновления")

        # Валидация опциональных параметров
        if summary is not None and (not isinstance(summary, str) or not summary.strip()):
            raise ValueError("summary должен быть непустой строкой")

        if team_access is not None and not isinstance(team_access, bool):
            raise ValueError("team_access должен быть boolean")

        if team_users is not None and not isinstance(team_users, list):
            raise ValueError("team_users должен быть списком строк")

        if clients is not None and not isinstance(clients, list):
            raise ValueError("clients должен быть списком строк")

        if followers is not None and not isinstance(followers, list):
            raise ValueError("followers должен быть списком строк")

        if tags is not None and not isinstance(tags, list):
            raise ValueError("tags должен быть списком строк")

        if parent_entity is not None:
            if not isinstance(parent_entity, dict):
                raise ValueError("parent_entity должен быть словарем")
            if "primary" not in parent_entity:
                raise ValueError("parent_entity должен содержать ключ 'primary'")

        if links is not None:
            if not isinstance(links, list):
                raise ValueError("links должен быть списком словарей")
            for link in links:
                if not isinstance(link, dict) or "relationship" not in link or "entity" not in link:
                    raise ValueError("каждая связь должна содержать ключи 'relationship' и 'entity'")

        # Валидация статуса в зависимости от типа сущности
        if entity_status is not None:
            valid_project_statuses = [
                "draft", "draft2", "in_progress", "according_to_plan",
                "postponed", "at_risk", "blocked", "launched", "cancelled"
            ]
            valid_goal_statuses = [
                "draft", "according_to_plan", "at_risk", "blocked",
                "achieved", "partially_achieved", "not_achieved", "exceeded", "cancelled"
            ]

            if entity_type in ["project", "portfolio"] and entity_status not in valid_project_statuses:
                raise ValueError(f"Для проектов/портфелей entity_status должен быть одним из: {', '.join(valid_project_statuses)}")
            elif entity_type == "goal" and entity_status not in valid_goal_statuses:
                raise ValueError(f"Для целей entity_status должен быть одним из: {', '.join(valid_goal_statuses)}")

        self.logger.info(f"Обновление сущности {entity_type}: {entity_id}")

        # Формирование полей для обновления
        fields = {}

        if summary is not None:
            fields["summary"] = summary

        if team_access is not None:
            fields["teamAccess"] = team_access

        if description is not None:
            fields["description"] = description

        if markup_type is not None:
            fields["markupType"] = markup_type

        if author is not None:
            fields["author"] = author

        if lead is not None:
            fields["lead"] = lead

        if team_users is not None:
            fields["teamUsers"] = team_users

        if clients is not None:
            fields["clients"] = clients

        if followers is not None:
            fields["followers"] = followers

        if start is not None:
            fields["start"] = start

        if end is not None:
            fields["end"] = end

        if tags is not None:
            fields["tags"] = tags

        if parent_entity is not None:
            fields["parentEntity"] = parent_entity

        if entity_status is not None:
            fields["entityStatus"] = entity_status

        # Формирование payload
        payload = {}

        if fields:
            payload["fields"] = fields

        if comment is not None:
            payload["comment"] = comment

        if links is not None:
            payload["links"] = links

        self.logger.debug(f"Параметры обновления сущности: {payload}")

        endpoint = f'/entities/{entity_type}/{entity_id}'
        result = await self._request(endpoint, 'PATCH', data=payload)

        entity_name = summary if summary else entity_id
        self.logger.info(f"Сущность {entity_type} '{entity_name}' успешно обновлена")

        return result

    async def delete(
        self,
        entity_type: EntityType,
        entity_id: str,
        with_board: bool = False
    ) -> Dict[str, Any]:
        """
        Удаление сущности (проект, портфель, цель).

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_id (str): Идентификатор сущности (id или shortId)
            with_board (bool): Удалить сущность вместе с доской
                              - True: удаляется сущность и связанная с ней доска
                              - False: удаляется только сущность (по умолчанию)

        Returns:
            Dict[str, Any]: Результат операции удаления

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если сущность не найдена
                - 403 если нет прав на удаление

        Examples:
            # Простое удаление проекта
            result = await client.entities.delete("project", "PROJECT-123")

            # Удаление портфеля вместе с доской
            result = await client.entities.delete(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                with_board=True
            )

            # Удаление цели
            result = await client.entities.delete("goal", "GOAL-789")
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(with_board, bool):
            raise ValueError("with_board должен быть boolean")

        self.logger.info(f"Удаление сущности {entity_type}: {entity_id} (с доской: {with_board})")

        endpoint = f'/entities/{entity_type}/{entity_id}'

        # Формирование параметров запроса
        params = {}
        if with_board:
            params['withBoard'] = 'true'

        self.logger.debug(f"Параметры удаления сущности: {params}")

        result = await self._request(endpoint, 'DELETE', params=params)

        self.logger.info(f"Сущность {entity_type} '{entity_id}' успешно удалена")

        return result

    async def search(
        self,
        entity_type: EntityType,
        fields: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        input: Optional[str] = None,
        filter: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_asc: Optional[bool] = None,
        root_only: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Поиск сущностей (проекты, портфели, цели) с фильтрацией и пагинацией.

        Args:
            entity_type (EntityType): Тип сущности для поиска
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            fields (Optional[str]): Дополнительные поля, которые будут включены в ответ
                                  Например: "entityStatus,summary,description"
            per_page (Optional[int]): Количество сущностей на странице ответа (по умолчанию 50)
            page (Optional[int]): Страница выдачи (по умолчанию 1)
            input (Optional[str]): Подстрока в названии сущности для поиска
            filter (Optional[Dict[str, Any]]): Параметры фильтрации
                                             Можно указать ключ любого поля и значение для фильтрации
                                             Например: {"author": "username", "entityStatus": "in_progress"}
            order_by (Optional[str]): Поле для сортировки
                                    Можно указать ключ любого поля
                                    Например: "summary", "createdAt", "updatedAt"
            order_asc (Optional[bool]): Направление сортировки
                                      - True: по возрастанию
                                      - False: по убыванию
            root_only (Optional[bool]): Выводить только не вложенные сущности
                                      - True: только корневые сущности
                                      - False: все сущности

        Returns:
            Dict[str, Any]: Результаты поиска с найденными сущностями и информацией о пагинации

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Examples:
            # Простой поиск проектов
            projects = await client.entities.search("project")

            # Поиск с фильтром по автору и статусу
            filtered_projects = await client.entities.search(
                entity_type="project",
                filter={"author": "username", "entityStatus": "in_progress"},
                fields="entityStatus,summary,description"
            )

            # Поиск портфелей с пагинацией и сортировкой
            portfolios = await client.entities.search(
                entity_type="portfolio",
                input="2025",
                per_page=20,
                page=2,
                order_by="createdAt",
                order_asc=False,
                root_only=True
            )

            # Поиск целей с комплексным фильтром
            goals = await client.entities.search(
                entity_type="goal",
                filter={
                    "lead": "manager",
                    "entityStatus": ["according_to_plan", "at_risk"]
                },
                fields="summary,entityStatus,start,end,lead",
                order_by="end",
                order_asc=True
            )
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        # Валидация опциональных параметров
        if fields is not None and not isinstance(fields, str):
            raise ValueError("fields должен быть строкой")

        if per_page is not None:
            if not isinstance(per_page, int) or per_page < 1 or per_page > 1000:
                raise ValueError("per_page должен быть числом от 1 до 1000")

        if page is not None:
            if not isinstance(page, int) or page < 1:
                raise ValueError("page должен быть числом больше 0")

        if input is not None and not isinstance(input, str):
            raise ValueError("input должен быть строкой")

        if filter is not None and not isinstance(filter, dict):
            raise ValueError("filter должен быть словарем")

        if order_by is not None and not isinstance(order_by, str):
            raise ValueError("order_by должен быть строкой")

        if order_asc is not None and not isinstance(order_asc, bool):
            raise ValueError("order_asc должен быть boolean")

        if root_only is not None and not isinstance(root_only, bool):
            raise ValueError("root_only должен быть boolean")

        self.logger.info(f"Поиск сущностей типа '{entity_type}' с фильтрами")

        endpoint = f'/entities/{entity_type}/_search'

        # Формирование параметров запроса
        params = {}

        if fields is not None:
            params['fields'] = fields

        if per_page is not None:
            params['perPage'] = per_page

        if page is not None:
            params['page'] = page

        # Формирование тела запроса
        payload = {}

        if input is not None:
            payload['input'] = input

        if filter is not None:
            payload['filter'] = filter

        if order_by is not None:
            payload['orderBy'] = order_by

        if order_asc is not None:
            payload['orderAsc'] = order_asc

        if root_only is not None:
            payload['rootOnly'] = root_only

        self.logger.debug(f"Параметры поиска сущностей - URL: {params}, Body: {payload}")

        # Если тело запроса пустое, отправляем пустой объект
        if not payload:
            payload = {}

        result = await self._request(endpoint, 'POST', params=params, data=payload)

        found_count = len(result.get('entities', []))
        self.logger.info(f"Найдено {found_count} сущностей типа '{entity_type}'")

        return result


    async def changelog(
        self,
        entity_type: EntityType,
        entity_id: str,
        per_page: Optional[int] = None,
        from_event: Optional[str] = None,
        selected: Optional[str] = None,
        new_events_on_top: Optional[bool] = None,
        direction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Получение истории изменений сущности (проект, портфель, цель).

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_id (str): Идентификатор сущности (id или shortId)
            per_page (Optional[int]): Максимальное количество событий в ответе (по умолчанию 50)
            from_event (Optional[str]): Идентификатор события, после которого начинает формироваться список
                                      Само событие в список не включается
                                      Не используется вместе с параметром selected
            selected (Optional[str]): Идентификатор события, вокруг которого формируется список
                                    Не указывается вместе с параметром from_event
                                    Список формируется в следующем порядке (для perPage=5):
                                    1. Событие с указанным идентификатором
                                    2. Событие, предшествующее первому событию
                                    3. Событие, следующее за первым событием
                                    4. Событие, предшествующее второму событию
                                    5. Событие, следующее за третьим событием
            new_events_on_top (Optional[bool]): Меняет порядок событий в списке на противоположный
                                               По умолчанию False (новые события внизу)
            direction (Optional[str]): Определяет порядок событий в списке
                                     - "forward" (по умолчанию) - прямой порядок
                                     - "backward" - инвертирует значение параметра new_events_on_top

        Returns:
            Dict[str, Any]: История событий сущности

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если сущность не найдена

        Examples:
            # Получение всей истории изменений проекта
            changelog = await client.entities.changelog("project", "PROJECT-123")

            # Получение последних 20 изменений портфеля
            recent_changes = await client.entities.changelog(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                per_page=20,
                new_events_on_top=True
            )

            # Получение изменений после определенного события
            changes_after = await client.entities.changelog(
                entity_type="goal",
                entity_id="GOAL-789",
                from_event="event_12345",
                per_page=10
            )

            # Получение изменений вокруг определенного события
            changes_around = await client.entities.changelog(
                entity_type="project",
                entity_id="PROJECT-123",
                selected="event_67890",
                per_page=5
            )

            # Получение изменений в обратном порядке
            backward_changes = await client.entities.changelog(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                direction="backward",
                per_page=15
            )
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        # Валидация опциональных параметров
        if per_page is not None:
            if not isinstance(per_page, int) or per_page < 1 or per_page > 1000:
                raise ValueError("per_page должен быть числом от 1 до 1000")

        if from_event is not None and not isinstance(from_event, str):
            raise ValueError("from_event должен быть строкой")

        if selected is not None and not isinstance(selected, str):
            raise ValueError("selected должен быть строкой")

        # Проверяем, что from_event и selected не используются одновременно
        if from_event is not None and selected is not None:
            raise ValueError("Параметры from_event и selected не могут использоваться одновременно")

        if new_events_on_top is not None and not isinstance(new_events_on_top, bool):
            raise ValueError("new_events_on_top должен быть boolean")

        if direction is not None:
            if not isinstance(direction, str) or direction not in ["forward", "backward"]:
                raise ValueError("direction должен быть одним из: forward, backward")

        self.logger.info(f"Получение истории изменений сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/events/_relative'

        # Формирование параметров запроса
        params = {}

        if per_page is not None:
            params['perPage'] = per_page

        if from_event is not None:
            params['from'] = from_event

        if selected is not None:
            params['selected'] = selected

        if new_events_on_top is not None:
            params['newEventsOnTop'] = 'true' if new_events_on_top else 'false'

        if direction is not None:
            params['direction'] = direction

        self.logger.debug(f"Параметры запроса истории изменений сущности: {params}")

        result = await self._request(endpoint, 'GET', params=params)

        events_count = len(result.get('events', []))
        self.logger.info(f"Получено {events_count} изменений для сущности {entity_type} '{entity_id}'")

        return result