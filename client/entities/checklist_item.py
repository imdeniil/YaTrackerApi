from typing import Dict, Any, Union, Optional
from ..base import BaseAPI

# Типы данных для отдельного пункта чеклиста
EntityType = str  # Тип сущности: project, portfolio, goal
AssigneeType = Union[str, int]  # Исполнитель пункта чеклиста
DeadlineType = Dict[str, str]  # Дедлайн пункта чеклиста

class ChecklistItemAPI(BaseAPI):
    """API для работы с отдельными пунктами чеклистов сущностей в Yandex Tracker"""

    async def update(
        self,
        entity_type: EntityType,
        entity_id: str,
        checklist_item_id: str,
        text: Optional[str] = None,
        checked: Optional[bool] = None,
        assignee: Optional[AssigneeType] = None,
        deadline: Optional[DeadlineType] = None,
        notify: Optional[bool] = None,
        notify_author: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Обновление конкретного пункта чеклиста сущности (проект, портфель, цель).

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_id (str): Идентификатор сущности (id или shortId)
            checklist_item_id (str): Идентификатор пункта чеклиста для обновления
            text (Optional[str]): Новый текст пункта чеклиста
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
            Dict[str, Any]: Информация об обновленном пункте чеклиста

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если сущность или пункт чеклиста не найден

        Examples:
            # Простое обновление текста пункта
            updated_item = await client.entities.checklists.item.update(
                entity_type="project",
                entity_id="PROJECT-123",
                checklist_item_id="658953a65c0f1b21abcdef01",
                text="Обновленный текст пункта"
            )

            # Отметка пункта как выполненного с назначением исполнителя
            completed_item = await client.entities.checklists.item.update(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                checklist_item_id="658953a65c0f1b21abcdef02",
                checked=True,
                assignee="project_manager"
            )

            # Установка дедлайна с уведомлениями
            item_with_deadline = await client.entities.checklists.item.update(
                entity_type="goal",
                entity_id="GOAL-789",
                checklist_item_id="658953a65c0f1b21abcdef03",
                deadline={
                    "date": "2025-12-31T23:59:59.000+0300",
                    "deadlineType": "date"
                },
                notify=True,
                notify_author=True,
                fields="summary,entityStatus",
                expand="attachments"
            )

            # Полное обновление пункта чеклиста
            fully_updated = await client.entities.checklists.item.update(
                entity_type="project",
                entity_id="PROJECT-123",
                checklist_item_id="658953a65c0f1b21abcdef04",
                text="Завершить интеграцию с API",
                checked=False,
                assignee=123456,  # ID пользователя
                deadline={
                    "date": "2025-01-15T18:00:00.000+0300",
                    "deadlineType": "date"
                }
            )
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(checklist_item_id, str) or not checklist_item_id.strip():
            raise ValueError("checklist_item_id должен быть непустой строкой")

        # Проверяем, что передан хотя бы один параметр для обновления
        update_params = [text, checked, assignee, deadline]
        if all(param is None for param in update_params):
            raise ValueError("Необходимо указать хотя бы один параметр для обновления: text, checked, assignee или deadline")

        # Валидация опциональных параметров
        if text is not None and (not isinstance(text, str) or not text.strip()):
            raise ValueError("text должен быть непустой строкой")

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

        self.logger.info(f"Обновление пункта чеклиста {checklist_item_id} для сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/checklistItems/{checklist_item_id}'

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
        payload = {}

        if text is not None:
            payload["text"] = text

        if checked is not None:
            payload["checked"] = checked

        if assignee is not None:
            payload["assignee"] = assignee

        if deadline is not None:
            payload["deadline"] = deadline

        self.logger.debug(f"Параметры обновления пункта чеклиста - URL: {params}, Body: {payload}")

        result = await self._request(endpoint, 'PATCH', params=params, data=payload)

        item_description = text if text else checklist_item_id
        self.logger.info(f"Пункт чеклиста '{item_description}' успешно обновлен для сущности {entity_type} '{entity_id}'")

        return result

    async def move(
        self,
        entity_type: EntityType,
        entity_id: str,
        checklist_item_id: str,
        before: str,
        notify: Optional[bool] = None,
        notify_author: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Перемещение пункта чеклиста сущности в другую позицию.

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_id (str): Идентификатор сущности (id или shortId)
            checklist_item_id (str): Идентификатор пункта чеклиста для перемещения
            before (str): Идентификатор пункта чеклиста, перед которым будет вставлен перемещаемый пункт
            notify (Optional[bool]): Уведомлять пользователей в полях Автор, Ответственный,
                                   Участники, Заказчики и Наблюдатели (по умолчанию True)
            notify_author (Optional[bool]): Уведомлять автора изменений (по умолчанию False)
            fields (Optional[str]): Дополнительные поля сущности для включения в ответ
            expand (Optional[str]): Дополнительная информация для включения в ответ
                                  - "attachments" - вложенные файлы

        Returns:
            Dict[str, Any]: Информация о перемещенном пункте чеклиста

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если сущность или пункт чеклиста не найден

        Examples:
            # Простое перемещение пункта чеклиста проекта
            moved_item = await client.entities.checklists.item.move(
                entity_type="project",
                entity_id="PROJECT-123",
                checklist_item_id="658953a65c0f1b21abcdef01",
                before="658953a65c0f1b21abcdef02"
            )

            # Перемещение с уведомлениями и дополнительными полями
            moved_with_notify = await client.entities.checklists.item.move(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                checklist_item_id="658953a65c0f1b21abcdef03",
                before="658953a65c0f1b21abcdef04",
                notify=True,
                notify_author=True,
                fields="summary,entityStatus",
                expand="attachments"
            )

            # Перемещение пункта чеклиста цели без уведомлений
            moved_goal_item = await client.entities.checklists.item.move(
                entity_type="goal",
                entity_id="GOAL-789",
                checklist_item_id="item_to_move",
                before="target_position_item",
                notify=False
            )
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(checklist_item_id, str) or not checklist_item_id.strip():
            raise ValueError("checklist_item_id должен быть непустой строкой")

        if not isinstance(before, str) or not before.strip():
            raise ValueError("before должен быть непустой строкой")

        # Валидация опциональных параметров
        if notify is not None and not isinstance(notify, bool):
            raise ValueError("notify должен быть boolean")

        if notify_author is not None and not isinstance(notify_author, bool):
            raise ValueError("notify_author должен быть boolean")

        if fields is not None and not isinstance(fields, str):
            raise ValueError("fields должен быть строкой")

        if expand is not None and not isinstance(expand, str):
            raise ValueError("expand должен быть строкой")

        self.logger.info(f"Перемещение пункта чеклиста {checklist_item_id} перед {before} для сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/checklistItems/{checklist_item_id}/_move'

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
            "before": before
        }

        self.logger.debug(f"Параметры перемещения пункта чеклиста - URL: {params}, Body: {payload}")

        result = await self._request(endpoint, 'POST', params=params, data=payload)

        self.logger.info(f"Пункт чеклиста '{checklist_item_id}' успешно перемещен для сущности {entity_type} '{entity_id}'")

        return result

    async def delete(
        self,
        entity_type: EntityType,
        entity_id: str,
        checklist_item_id: str,
        notify: Optional[bool] = None,
        notify_author: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Удаление пункта чеклиста сущности (проект, портфель, цель).

        Args:
            entity_type (EntityType): Тип сущности
                                    - "project" - проект
                                    - "portfolio" - портфель
                                    - "goal" - цель
            entity_id (str): Идентификатор сущности (id или shortId)
            checklist_item_id (str): Идентификатор пункта чеклиста для удаления
            notify (Optional[bool]): Уведомлять пользователей в полях Автор, Ответственный,
                                   Участники, Заказчики и Наблюдатели (по умолчанию True)
            notify_author (Optional[bool]): Уведомлять автора изменений (по умолчанию False)
            fields (Optional[str]): Дополнительные поля сущности для включения в ответ
            expand (Optional[str]): Дополнительная информация для включения в ответ
                                  - "attachments" - вложенные файлы

        Returns:
            Dict[str, Any]: Информация об удаленном пункте чеклиста

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если сущность или пункт чеклиста не найден

        Examples:
            # Простое удаление пункта чеклиста проекта
            result = await client.entities.checklists.item.delete(
                entity_type="project",
                entity_id="PROJECT-123",
                checklist_item_id="658953a65c0f1b21abcdef01"
            )

            # Удаление с отключением уведомлений
            result = await client.entities.checklists.item.delete(
                entity_type="portfolio",
                entity_id="PORTFOLIO-456",
                checklist_item_id="658953a65c0f1b21abcdef02",
                notify=False
            )

            # Удаление с дополнительными полями в ответе
            result = await client.entities.checklists.item.delete(
                entity_type="goal",
                entity_id="GOAL-789",
                checklist_item_id="658953a65c0f1b21abcdef03",
                notify=True,
                notify_author=True,
                fields="summary,entityStatus",
                expand="attachments"
            )

            # Проверка результата удаления
            if result:
                print(f"Пункт чеклиста {checklist_item_id} успешно удален")

            # Массовое удаление пунктов (в цикле)
            items_to_delete = ["item_01", "item_02", "item_03"]
            for item_id in items_to_delete:
                try:
                    await client.entities.checklists.item.delete(
                        entity_type="project",
                        entity_id="PROJECT-123",
                        checklist_item_id=item_id
                    )
                    print(f"Удален пункт {item_id}")
                except Exception as e:
                    print(f"Ошибка при удалении пункта {item_id}: {e}")

            # Удаление с проверкой существования
            try:
                await client.entities.checklists.item.delete(
                    entity_type="portfolio",
                    entity_id="PORTFOLIO-456",
                    checklist_item_id="non_existent_item"
                )
            except Exception as e:
                print(f"Пункт не найден или уже удален: {e}")
        """
        # Валидация обязательных параметров
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(checklist_item_id, str) or not checklist_item_id.strip():
            raise ValueError("checklist_item_id должен быть непустой строкой")

        # Валидация опциональных параметров
        if notify is not None and not isinstance(notify, bool):
            raise ValueError("notify должен быть boolean")

        if notify_author is not None and not isinstance(notify_author, bool):
            raise ValueError("notify_author должен быть boolean")

        if fields is not None and not isinstance(fields, str):
            raise ValueError("fields должен быть строкой")

        if expand is not None and not isinstance(expand, str):
            raise ValueError("expand должен быть строкой")

        self.logger.info(f"Удаление пункта чеклиста {checklist_item_id} для сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/checklistItems/{checklist_item_id}'

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

        self.logger.debug(f"Параметры удаления пункта чеклиста - URL: {params}")

        result = await self._request(endpoint, 'DELETE', params=params)

        self.logger.info(f"Пункт чеклиста '{checklist_item_id}' успешно удален для сущности {entity_type} '{entity_id}'")

        return result