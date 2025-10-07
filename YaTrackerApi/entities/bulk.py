from typing import List, Dict, Any, Optional
from ..base import BaseAPI

# Типы данных для массовых операций
EntityType = str  # Тип сущности: project, portfolio, goal
EntityLinkType = Dict[str, str]  # Связь с другой сущностью

class BulkAPI(BaseAPI):
    """API для массовых операций с сущностями в Yandex Tracker"""

    async def update(
        self,
        entity_type: EntityType,
        entity_ids: List[str],
        fields: Optional[Dict[str, Any]] = None,
        comment: Optional[str] = None,
        links: Optional[List[EntityLinkType]] = None
    ) -> Dict[str, Any]:
        """
        Массовое обновление сущностей (проекты, портфели, цели).

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_ids (List[str]): Список идентификаторов сущностей для обновления
            fields (Optional[Dict[str, Any]]): Поля для обновления
                                             Объект с парами "поле-значение"
                                             Например: {"summary": "Новое название", "entityStatus": "in_progress"}
            comment (Optional[str]): Комментарий к массовому обновлению
            links (Optional[List[EntityLinkType]]): Настройки связей с другими сущностями
                                                  [{"relationship": "depends on", "entity": "entity_id"}]

        Returns:
            Dict[str, Any]: Результат массового обновления

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Examples:
            # Простое массовое обновление проектов
            result = await client.entities.bulk.update(
                entity_type="project",
                entity_ids=["PROJECT-123", "PROJECT-124", "PROJECT-125"],
                fields={"entityStatus": "in_progress"},
                comment="Перевод проектов в статус 'В работе'"
            )

            # Массовое обновление портфелей с полями и связями
            result = await client.entities.bulk.update(
                entity_type="portfolio",
                entity_ids=["PORTFOLIO-456", "PORTFOLIO-457"],
                fields={
                    "entityStatus": "according_to_plan",
                    "lead": "new_manager"
                },
                comment="Обновление менеджера портфелей",
                links=[
                    {"relationship": "depends on", "entity": "GOAL-789"}
                ]
            )

            # Массовое обновление целей с установкой родительской цели
            result = await client.entities.bulk.update(
                entity_type="goal",
                entity_ids=["GOAL-100", "GOAL-101"],
                fields={"entityStatus": "achieved"},
                links=[
                    {"relationship": "parent entity", "entity": "GOAL-PARENT"}
                ],
                comment="Цели достигнуты, установлена родительская цель"
            )
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_ids, list) or not entity_ids:
            raise ValueError("entity_ids должен быть непустым списком")

        for entity_id in entity_ids:
            if not isinstance(entity_id, str) or not entity_id.strip():
                raise ValueError("Все элементы entity_ids должны быть непустыми строками")

        # Проверяем, что передан хотя бы один параметр для обновления
        if fields is None and comment is None and links is None:
            raise ValueError("Необходимо указать хотя бы один параметр для обновления: fields, comment или links")

        # Валидация опциональных параметров
        if fields is not None and not isinstance(fields, dict):
            raise ValueError("fields должен быть словарем")

        if comment is not None and not isinstance(comment, str):
            raise ValueError("comment должен быть строкой")

        if links is not None:
            if not isinstance(links, list):
                raise ValueError("links должен быть списком словарей")

            # Валидация типов связей в зависимости от типа сущности
            valid_project_portfolio_relationships = [
                "depends on", "is dependent by", "works towards"
            ]
            valid_goal_relationships = [
                "parent entity", "child entity", "depends on",
                "is dependent by", "is supported by"
            ]

            for link in links:
                if not isinstance(link, dict) or "relationship" not in link or "entity" not in link:
                    raise ValueError("каждая связь должна содержать ключи 'relationship' и 'entity'")

                relationship = link["relationship"]
                if entity_type in ["project", "portfolio"]:
                    if relationship not in valid_project_portfolio_relationships:
                        raise ValueError(f"Для проектов/портфелей relationship должен быть одним из: {', '.join(valid_project_portfolio_relationships)}")
                elif entity_type == "goal":
                    if relationship not in valid_goal_relationships:
                        raise ValueError(f"Для целей relationship должен быть одним из: {', '.join(valid_goal_relationships)}")

        self.logger.info(f"Массовое обновление {len(entity_ids)} сущностей типа '{entity_type}'")

        endpoint = f'/entities/{entity_type}/bulkchange/_update'

        # Формирование тела запроса
        payload = {
            "metaEntities": entity_ids
        }

        values = {}

        if fields is not None:
            values["fields"] = fields

        if comment is not None:
            values["comment"] = comment

        if links is not None:
            values["links"] = links

        if values:
            payload["values"] = values

        self.logger.debug(f"Параметры массового обновления сущностей: {payload}")

        result = await self._request(endpoint, 'POST', data=payload)

        self.logger.info(f"Массовое обновление {len(entity_ids)} сущностей типа '{entity_type}' успешно выполнено")

        return result