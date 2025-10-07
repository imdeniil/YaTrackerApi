from typing import List, Dict, Any, Union, Optional
from ..base import BaseAPI

# Типы данных для чеклистов сущностей
EntityType = str  # Тип сущности: project, portfolio, goal
AssigneeType = Union[str, int]  # Исполнитель пункта чеклиста
DeadlineType = Dict[str, str]  # Дедлайн пункта чеклиста

class EntityChecklistsAPI(BaseAPI):
    """API для работы с чеклистами сущностей (проекты, портфели, цели) в Yandex Tracker"""

    @property
    def item(self):
        """API для работы с отдельными пунктами чеклистов"""
        if not hasattr(self, '_item'):
            from .checklist_item import ChecklistItemAPI
            self._item = ChecklistItemAPI(self.client)
        return self._item

    async def create(
        self,
        entity_type: EntityType,
        entity_id: str,
        text: str,
        checked: Optional[bool] = None,
        assignee: Optional[AssigneeType] = None,
        deadline: Optional[DeadlineType] = None,
        notify: Optional[bool] = None,
        notify_author: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Создание пункта чеклиста для сущности (проект, портфель, цель).

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_id (str): Идентификатор сущности (id или shortId)
            text (str): Текст пункта чеклиста (обязательное поле)
            checked (Optional[bool]): Отметка о выполнении пункта
                                    - True: пункт отмечен как выполненный
                                    - False: пункт не отмечен как выполненный
            assignee (Optional[AssigneeType]): Идентификатор или логин исполнителя пункта
            deadline (Optional[DeadlineType]): Дедлайн пункта чеклиста
                                             {"date": "YYYY-MM-DDThh:mm:ss.sss±hhmm", "deadlineType": "date"}
            notify (Optional[bool]): Уведомлять пользователей в полях Автор, Ответственный,
                                   Участники, Заказчики и Наблюдатели (по умолчанию True)
            notify_author (Optional[bool]): Уведомлять автора изменений (по умолчанию False)
            fields (Optional[str]): Дополнительные поля сущности для включения в ответ
            expand (Optional[str]): Дополнительная информация для включения в ответ
                                  - "attachments" - вложенные файлы

        Returns:
            Dict[str, Any]: Информация о созданном пункте чеклиста

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если сущность не найдена

        Examples:
            # Простое создание пункта чеклиста проекта
            item = await client.entities.checklists.create(
                entity_type="project",
                entity_id="PROJECT-123",
                text="Подготовить техническое задание"
            )

            # Создание выполненного пункта с исполнителем
            completed_item = await client.entities.checklists.create(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                text="Провести анализ рисков",
                checked=True,
                assignee="analyst_user"
            )

            # Создание пункта с дедлайном и уведомлениями
            deadline_item = await client.entities.checklists.create(
                entity_type="goal",
                entity_id="GOAL-789",
                text="Завершить разработку MVP",
                assignee="developer123",
                deadline={
                    "date": "2025-12-31T23:59:59.000+0300",
                    "deadlineType": "date"
                },
                notify=True,
                notify_author=True,
                fields="summary,entityStatus",
                expand="attachments"
            )

            # Создание пункта для портфеля с исполнителем по ID
            item_with_id = await client.entities.checklists.create(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                text="Обновить бюджет проекта",
                assignee=123456,  # ID пользователя
                checked=False
            )
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(text, str) or not text.strip():
            raise ValueError("text должен быть непустой строкой")

        # Валидация опциональных параметров
        if checked is not None and not isinstance(checked, bool):
            raise ValueError("checked должен быть boolean")

        if assignee is not None and not isinstance(assignee, (str, int)):
            raise ValueError("assignee должен быть строкой или числом")

        if assignee is not None and isinstance(assignee, str) and not assignee.strip():
            raise ValueError("assignee (строка) должен быть непустым")

        if deadline is not None:
            if not isinstance(deadline, dict):
                raise ValueError("deadline должен быть словарем")
            if "date" not in deadline or "deadlineType" not in deadline:
                raise ValueError("deadline должен содержать ключи 'date' и 'deadlineType'")
            if not isinstance(deadline["date"], str) or not deadline["date"].strip():
                raise ValueError("deadline['date'] должен быть непустой строкой")
            if not isinstance(deadline["deadlineType"], str) or not deadline["deadlineType"].strip():
                raise ValueError("deadline['deadlineType'] должен быть непустой строкой")

        if notify is not None and not isinstance(notify, bool):
            raise ValueError("notify должен быть boolean")

        if notify_author is not None and not isinstance(notify_author, bool):
            raise ValueError("notify_author должен быть boolean")

        if fields is not None and not isinstance(fields, str):
            raise ValueError("fields должен быть строкой")

        if expand is not None and not isinstance(expand, str):
            raise ValueError("expand должен быть строкой")

        self.logger.info(f"Создание пункта чеклиста для сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/checklistItems'

        # Формирование параметров запроса
        params = {}

        if notify is not None:
            params['notify'] = 'true' if notify else 'false'

        if notify_author is not None:
            params['notifyAuthor'] = 'true' if notify_author else 'false'

        if fields is not None:
            params['fields'] = fields

        if expand is not None:
            params['expand'] = expand

        # Формирование тела запроса
        payload = {
            "text": text
        }

        if checked is not None:
            payload["checked"] = checked

        if assignee is not None:
            payload["assignee"] = assignee

        if deadline is not None:
            payload["deadline"] = deadline

        self.logger.debug(f"Параметры создания пункта чеклиста - URL: {params}, Body: {payload}")

        result = await self._request(endpoint, 'POST', params=params, data=payload)

        self.logger.info(f"Пункт чеклиста '{text}' успешно создан для сущности {entity_type} '{entity_id}'")

        return result

    async def update(
        self,
        entity_type: EntityType,
        entity_id: str,
        checklist_items: List[Dict[str, Any]],
        notify: Optional[bool] = None,
        notify_author: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Массовое обновление пунктов чеклиста сущности (проект, портфель, цель).

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_id (str): Идентификатор сущности (id или shortId)
            checklist_items (List[Dict[str, Any]]): Список пунктов чеклиста для обновления
                                                   Каждый элемент должен содержать:
                                                   - "id": идентификатор пункта (обязательно)
                                                   - "text": текст пункта (опционально)
                                                   - "checked": отметка о выполнении (опционально)
                                                   - "assignee": исполнитель (опционально)
                                                   - "deadline": дедлайн (опционально)
            notify (Optional[bool]): Уведомлять пользователей в полях Автор, Ответственный,
                                   Участники, Заказчики и Наблюдатели (по умолчанию True)
            notify_author (Optional[bool]): Уведомлять автора изменений (по умолчанию False)
            fields (Optional[str]): Дополнительные поля сущности для включения в ответ
            expand (Optional[str]): Дополнительная информация для включения в ответ
                                  - "attachments" - вложенные файлы

        Returns:
            Dict[str, Any]: Информация об обновленных пунктах чеклиста

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если сущность не найдена

        Examples:
            # Простое обновление текста и статуса пунктов
            updated_items = await client.entities.checklists.update(
                entity_type="project",
                entity_id="PROJECT-123",
                checklist_items=[
                    {
                        "id": "658953a65c0f1b21abcdef01",
                        "text": "Обновленное задание 1",
                        "checked": True
                    },
                    {
                        "id": "658953a65c0f1b21abcdef02",
                        "text": "Обновленное задание 2",
                        "checked": False,
                        "assignee": "new_assignee"
                    }
                ]
            )

            # Обновление с установкой дедлайнов и исполнителей
            updated_with_deadline = await client.entities.checklists.update(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                checklist_items=[
                    {
                        "id": "658953a65c0f1b21abcdef03",
                        "checked": True,
                        "assignee": "project_manager",
                        "deadline": {
                            "date": "2025-12-31T23:59:59.000+0300",
                            "deadlineType": "date"
                        }
                    }
                ],
                notify=True,
                notify_author=True,
                fields="summary,entityStatus",
                expand="attachments"
            )

            # Массовое обновление статуса выполнения
            bulk_complete = await client.entities.checklists.update(
                entity_type="goal",
                entity_id="GOAL-789",
                checklist_items=[
                    {"id": "item_01", "checked": True},
                    {"id": "item_02", "checked": True},
                    {"id": "item_03", "checked": False, "assignee": 123456}
                ]
            )
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(checklist_items, list) or not checklist_items:
            raise ValueError("checklist_items должен быть непустым списком")

        # Валидация каждого элемента чеклиста
        for i, item in enumerate(checklist_items):
            if not isinstance(item, dict):
                raise ValueError(f"Элемент {i} в checklist_items должен быть словарем")

            if "id" not in item:
                raise ValueError(f"Элемент {i} в checklist_items должен содержать поле 'id'")

            if not isinstance(item["id"], str) or not item["id"].strip():
                raise ValueError(f"Поле 'id' в элементе {i} должно быть непустой строкой")

            # Валидация опциональных полей элемента
            if "text" in item:
                if not isinstance(item["text"], str) or not item["text"].strip():
                    raise ValueError(f"Поле 'text' в элементе {i} должно быть непустой строкой")

            if "checked" in item and not isinstance(item["checked"], bool):
                raise ValueError(f"Поле 'checked' в элементе {i} должно быть boolean")

            if "assignee" in item:
                if not isinstance(item["assignee"], (str, int)):
                    raise ValueError(f"Поле 'assignee' в элементе {i} должно быть строкой или числом")
                if isinstance(item["assignee"], str) and not item["assignee"].strip():
                    raise ValueError(f"Поле 'assignee' (строка) в элементе {i} должно быть непустым")

            if "deadline" in item:
                deadline = item["deadline"]
                if not isinstance(deadline, dict):
                    raise ValueError(f"Поле 'deadline' в элементе {i} должно быть словарем")
                if "date" not in deadline or "deadlineType" not in deadline:
                    raise ValueError(f"Поле 'deadline' в элементе {i} должно содержать ключи 'date' и 'deadlineType'")
                if not isinstance(deadline["date"], str) or not deadline["date"].strip():
                    raise ValueError(f"deadline['date'] в элементе {i} должен быть непустой строкой")
                if not isinstance(deadline["deadlineType"], str) or not deadline["deadlineType"].strip():
                    raise ValueError(f"deadline['deadlineType'] в элементе {i} должен быть непустой строкой")

        # Валидация опциональных параметров
        if notify is not None and not isinstance(notify, bool):
            raise ValueError("notify должен быть boolean")

        if notify_author is not None and not isinstance(notify_author, bool):
            raise ValueError("notify_author должен быть boolean")

        if fields is not None and not isinstance(fields, str):
            raise ValueError("fields должен быть строкой")

        if expand is not None and not isinstance(expand, str):
            raise ValueError("expand должен быть строкой")

        self.logger.info(f"Обновление {len(checklist_items)} пунктов чеклиста для сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/checklistItems'

        # Формирование параметров запроса
        params = {}

        if notify is not None:
            params['notify'] = 'true' if notify else 'false'

        if notify_author is not None:
            params['notifyAuthor'] = 'true' if notify_author else 'false'

        if fields is not None:
            params['fields'] = fields

        if expand is not None:
            params['expand'] = expand

        # Тело запроса - это массив элементов чеклиста
        payload = checklist_items

        self.logger.debug(f"Параметры обновления чеклиста - URL: {params}, Body: {len(payload)} элементов")

        result = await self._request(endpoint, 'PATCH', params=params, data=payload)

        self.logger.info(f"Успешно обновлено {len(checklist_items)} пунктов чеклиста для сущности {entity_type} '{entity_id}'")

        return result