from typing import Dict, Any, List, Optional
from ..base import BaseAPI

# Типы данных для связей сущностей
EntityType = str  # Тип сущности: project, portfolio, goal
RelationshipType = str  # Тип связи между сущностями

class LinksAPI(BaseAPI):
    """API для работы со связями сущностей в Yandex Tracker"""

    async def create(
        self,
        entity_type: EntityType,
        entity_id: str,
        relationship: RelationshipType,
        entity: str
    ) -> Dict[str, Any]:
        """
        Создание связи между сущностями (проекты, портфели, цели).

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_id (str): Идентификатор сущности (id или shortId)
            relationship (RelationshipType): Тип связи
                                           Для проектов и портфелей:
                                           - "depends on" - текущая сущность зависит от связанной
                                           - "is dependent by" - текущая сущность блокирует связанную
                                           - "works towards" - связь проекта с целью

                                           Для целей:
                                           - "parent entity" - родительская цель
                                           - "child entity" - подцель
                                           - "depends on" - текущая цель зависит от связанной
                                           - "is dependent by" - текущая цель блокирует связанную
                                           - "is supported by" - связь с проектом
            entity (str): Идентификатор связываемой сущности

        Returns:
            Dict[str, Any]: Информация о созданной связи

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если сущность не найдена

        Examples:
            # Создание зависимости между проектами
            link = await client.entities.links.create(
                entity_type="project",
                entity_id="PROJECT-123",
                relationship="depends on",
                entity="PROJECT-456"
            )

            # Проект блокирует другой проект
            blocking_link = await client.entities.links.create(
                entity_type="project",
                entity_id="PROJECT-123",
                relationship="is dependent by",
                entity="PROJECT-789"
            )

            # Проект работает для достижения цели
            goal_link = await client.entities.links.create(
                entity_type="project",
                entity_id="PROJECT-123",
                relationship="works towards",
                entity="GOAL-001"
            )

            # Связь портфеля с целью
            portfolio_goal = await client.entities.links.create(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                relationship="works towards",
                entity="GOAL-002"
            )

            # Создание родительско-дочерней связи для целей
            parent_goal = await client.entities.links.create(
                entity_type="goal",
                entity_id="GOAL-CHILD",
                relationship="parent entity",
                entity="GOAL-PARENT"
            )

            # Подцель для родительской цели
            child_goal = await client.entities.links.create(
                entity_type="goal",
                entity_id="GOAL-PARENT",
                relationship="child entity",
                entity="GOAL-CHILD-02"
            )

            # Зависимость между целями
            goal_dependency = await client.entities.links.create(
                entity_type="goal",
                entity_id="GOAL-A",
                relationship="depends on",
                entity="GOAL-B"
            )

            # Цель поддерживается проектом
            supported_goal = await client.entities.links.create(
                entity_type="goal",
                entity_id="GOAL-001",
                relationship="is supported by",
                entity="PROJECT-SUPPORT"
            )

            # Результат содержит информацию о созданной связи
            print(f"Создана связь: {link['relationship']} с сущностью {link['entity']}")
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(relationship, str) or not relationship.strip():
            raise ValueError("relationship должен быть непустой строкой")

        if not isinstance(entity, str) or not entity.strip():
            raise ValueError("entity должен быть непустой строкой")

        # Валидация типов связей в зависимости от типа сущности
        valid_project_portfolio_relationships = [
            "depends on", "is dependent by", "works towards"
        ]
        valid_goal_relationships = [
            "parent entity", "child entity", "depends on",
            "is dependent by", "is supported by"
        ]

        if entity_type in ["project", "portfolio"]:
            if relationship not in valid_project_portfolio_relationships:
                raise ValueError(f"Для проектов/портфелей relationship должен быть одним из: {', '.join(valid_project_portfolio_relationships)}")
        elif entity_type == "goal":
            if relationship not in valid_goal_relationships:
                raise ValueError(f"Для целей relationship должен быть одним из: {', '.join(valid_goal_relationships)}")

        self.logger.info(f"Создание связи '{relationship}' для сущности {entity_type}: {entity_id} -> {entity}")

        endpoint = f'/entities/{entity_type}/{entity_id}/links'

        # Формирование тела запроса
        payload = {
            "relationship": relationship,
            "entity": entity
        }

        self.logger.debug(f"Параметры создания связи - Body: {payload}")

        result = await self._request(endpoint, 'POST', data=payload)

        self.logger.info(f"Связь '{relationship}' успешно создана для сущности {entity_type} '{entity_id}' с сущностью '{entity}'")

        return result

    async def get(
        self,
        entity_type: EntityType,
        entity_id: str,
        fields: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Получение связей сущности (проект, портфель, цель).

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_id (str): Идентификатор сущности (id или shortId)
            fields (Optional[str]): Поля связанных сущностей, которые будут включены в ответ
                                  Список допустимых полей через запятую
                                  Например: "id,key,summary,entityStatus"

        Returns:
            List[Dict[str, Any]]: Список связей сущности с их информацией

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если сущность не найдена

        Examples:
            # Получение всех связей проекта
            links = await client.entities.links.get(
                entity_type="project",
                entity_id="PROJECT-123"
            )

            # Получение связей с дополнительными полями
            detailed_links = await client.entities.links.get(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                fields="id,key,summary,entityStatus,lead"
            )

            # Получение связей цели
            goal_links = await client.entities.links.get(
                entity_type="goal",
                entity_id="GOAL-789"
            )

            # Анализ полученных связей
            for link in links:
                relationship = link['object']['relationship']
                linked_entity = link['object']['entity']
                direction = link['direction']

                print(f"Связь: {relationship}")
                print(f"Направление: {direction}")
                print(f"Связанная сущность: {linked_entity}")

                # Если запрошены дополнительные поля
                if 'summary' in linked_entity:
                    print(f"Название: {linked_entity['summary']}")

                if 'entityStatus' in linked_entity:
                    status_name = linked_entity['entityStatus']['name']
                    print(f"Статус: {status_name}")

            # Фильтрация связей по типу
            dependency_links = [
                link for link in links
                if link['object']['relationship'] in ['depends on', 'is dependent by']
            ]

            print(f"Найдено {len(dependency_links)} связей зависимостей")

            # Поиск связей с определенным типом сущностей
            project_links = [
                link for link in links
                if link['object']['entity'].get('entityType') == 'project'
            ]

            goal_links = [
                link for link in links
                if link['object']['entity'].get('entityType') == 'goal'
            ]

            print(f"Связей с проектами: {len(project_links)}")
            print(f"Связей с целями: {len(goal_links)}")

            # Получение входящих и исходящих связей
            outward_links = [link for link in links if link['direction'] == 'outward']
            inward_links = [link for link in links if link['direction'] == 'inward']

            print(f"Исходящих связей: {len(outward_links)}")
            print(f"Входящих связей: {len(inward_links)}")
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        # Валидация опциональных параметров
        if fields is not None and not isinstance(fields, str):
            raise ValueError("fields должен быть строкой")

        self.logger.info(f"Получение связей для сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/links'

        # Формирование параметров запроса
        params = {}

        if fields is not None:
            params['fields'] = fields

        self.logger.debug(f"Параметры получения связей - URL: {params}")

        result = await self._request(endpoint, 'GET', params=params)

        # Проверяем, что получили список
        if not isinstance(result, list):
            self.logger.warning(f"Неожиданный тип ответа: {type(result)}")
            result = []

        links_count = len(result)
        self.logger.info(f"Получено {links_count} связей для сущности {entity_type} '{entity_id}'")

        if links_count > 0:
            # Анализируем связи для логирования
            relationship_types = set()
            directions = {'inward': 0, 'outward': 0}
            linked_entity_types = set()

            for link in result:
                if 'object' in link and 'relationship' in link['object']:
                    relationship_types.add(link['object']['relationship'])

                if 'direction' in link:
                    direction = link['direction']
                    directions[direction] = directions.get(direction, 0) + 1

                if ('object' in link and 'entity' in link['object'] and
                    'entityType' in link['object']['entity']):
                    linked_entity_types.add(link['object']['entity']['entityType'])

            self.logger.debug(f"Типы связей: {', '.join(relationship_types)}")
            self.logger.debug(f"Направления: исходящих {directions.get('outward', 0)}, входящих {directions.get('inward', 0)}")

            if linked_entity_types:
                self.logger.debug(f"Связанные типы сущностей: {', '.join(linked_entity_types)}")

        return result

    async def delete(
        self,
        entity_type: EntityType,
        entity_id: str,
        right: str
    ) -> Dict[str, Any]:
        """
        Удаление связи между сущностями (проекты, портфели, цели).

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_id (str): Идентификатор текущей сущности (id или shortId)
            right (str): Идентификатор сущности, с которой удаляется связь

        Returns:
            Dict[str, Any]: Информация об удалении связи

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если сущность не найдена
                - 422 если связь не существует

        Examples:
            # Удаление связи между проектами
            result = await client.entities.links.delete(
                entity_type="project",
                entity_id="PROJECT-123",
                right="PROJECT-456"
            )

            # Удаление связи проекта с целью
            result = await client.entities.links.delete(
                entity_type="project",
                entity_id="PROJECT-123",
                right="GOAL-001"
            )

            # Удаление связи между портфелем и целью
            result = await client.entities.links.delete(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                right="GOAL-002"
            )

            # Удаление родительско-дочерней связи между целями
            result = await client.entities.links.delete(
                entity_type="goal",
                entity_id="GOAL-CHILD",
                right="GOAL-PARENT"
            )

            # Удаление связи зависимости между целями
            result = await client.entities.links.delete(
                entity_type="goal",
                entity_id="GOAL-A",
                right="GOAL-B"
            )

            # Проверка результата удаления
            if result:
                print(f"Связь между {entity_id} и {right} успешно удалена")

            # Массовое удаление связей
            entities_to_unlink = ["PROJECT-456", "PROJECT-789", "GOAL-001"]

            for linked_entity in entities_to_unlink:
                try:
                    await client.entities.links.delete(
                        entity_type="project",
                        entity_id="PROJECT-123",
                        right=linked_entity
                    )
                    print(f"Удалена связь с {linked_entity}")
                except Exception as e:
                    print(f"Ошибка при удалении связи с {linked_entity}: {e}")

            # Удаление связи с проверкой существования
            try:
                await client.entities.links.delete(
                    entity_type="portfolio",
                    entity_id="PORTFOLIO-456",
                    right="NON-EXISTENT-ENTITY"
                )
            except Exception as e:
                print(f"Связь не найдена или не может быть удалена: {e}")

            # Очистка всех связей определенного типа
            # Сначала получаем все связи
            links = await client.entities.links.get(
                entity_type="project",
                entity_id="PROJECT-123"
            )

            # Удаляем связи с целями
            goal_links = [
                link for link in links
                if link['object']['entity'].get('entityType') == 'goal'
            ]

            for link in goal_links:
                linked_entity_id = link['object']['entity']['id']
                await client.entities.links.delete(
                    entity_type="project",
                    entity_id="PROJECT-123",
                    right=linked_entity_id
                )
                print(f"Удалена связь с целью {linked_entity_id}")
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(right, str) or not right.strip():
            raise ValueError("right должен быть непустой строкой")

        self.logger.info(f"Удаление связи для сущности {entity_type}: {entity_id} с сущностью {right}")

        endpoint = f'/entities/{entity_type}/{entity_id}/links'

        # Формирование параметров запроса
        params = {
            'right': right
        }

        self.logger.debug(f"Параметры удаления связи - URL: {params}")

        result = await self._request(endpoint, 'DELETE', params=params)

        self.logger.info(f"Связь успешно удалена между сущностью {entity_type} '{entity_id}' и сущностью '{right}'")

        return result