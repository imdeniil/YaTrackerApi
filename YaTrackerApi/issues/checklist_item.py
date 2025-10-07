"""
API модуль для работы с отдельными пунктами чеклистов задач в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class ChecklistItemAPI(BaseAPI):
    """API для работы с отдельными пунктами чеклистов задач в Yandex Tracker"""

    async def update(
        self,
        issue_id: str,
        item_id: str,
        text: str,
        checked: Optional[bool] = None,
        assignee: Optional[Union[str, int, Dict[str, Union[str, int]]]] = None,
        deadline: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Обновление пункта чеклиста задачи

        Обновляет указанный пункт чеклиста, но требует передачи всех пунктов
        в теле запроса. API Yandex Tracker требует указать все пункты чеклиста,
        включая обновляемый.

        Args:
            issue_id: Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')
            item_id: Идентификатор пункта чеклиста для обновления
            text: Новый текст пункта чеклиста (обязательный параметр)
            checked: Новый статус выполнения пункта:
                - True: пункт отмечен как выполненный
                - False: пункт не отмечен как выполненный
                - None: оставить текущий статус
            assignee: Новый исполнитель пункта чеклиста:
                - Строка: логин пользователя
                - Число: ID пользователя
                - Объект: {"login": "username"} или {"id": "123"}
                - None: убрать исполнителя
            deadline: Новый дедлайн пункта чеклиста:
                - {"date": "2021-05-09T00:00:00.000+0000", "deadlineType": "date"}
                - None: убрать дедлайн

        Returns:
            List[Dict]: Обновленный список всех пунктов чеклиста

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404, 400, 403)
            ValueError: При некорректных параметрах

        Examples:
            # Обновление текста пункта
            updated_checklist = await client.issues.checklists.item.update(
                'TASK-123',
                'item_id_123',
                'Обновленный текст пункта'
            )

            # Отметить пункт как выполненный
            updated_checklist = await client.issues.checklists.item.update(
                'TASK-123',
                'item_id_123',
                'Задача выполнена',
                checked=True
            )

            # Назначить исполнителя
            updated_checklist = await client.issues.checklists.item.update(
                'TASK-123',
                'item_id_123',
                'Провести тестирование',
                assignee='tester1'
            )

            # Полное обновление с дедлайном
            updated_checklist = await client.issues.checklists.item.update(
                'TASK-123',
                'item_id_123',
                'Подготовить отчет до конца месяца',
                checked=False,
                assignee={'login': 'analyst'},
                deadline={
                    'date': '2025-12-31T17:00:00.000+0000',
                    'deadlineType': 'date'
                }
            )

            # Убрать исполнителя и дедлайн
            updated_checklist = await client.issues.checklists.item.update(
                'TASK-123',
                'item_id_123',
                'Задача без назначений',
                assignee=None,
                deadline=None
            )

            # Результат содержит весь обновленный чеклист
            updated_item = next(
                (item for item in updated_checklist if item['id'] == 'item_id_123'),
                None
            )
            print(f"Обновленный пункт: {updated_item['text']}")
        """

        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        if not item_id or not isinstance(item_id, str):
            raise ValueError("item_id должен быть непустой строкой")

        if not text or not isinstance(text, str):
            raise ValueError("text должен быть непустой строкой")

        if checked is not None and not isinstance(checked, bool):
            raise ValueError("checked должен быть логическим значением")

        if deadline is not None:
            if not isinstance(deadline, dict):
                raise ValueError("deadline должен быть словарем")
            if 'date' not in deadline or 'deadlineType' not in deadline:
                raise ValueError("deadline должен содержать поля 'date' и 'deadlineType'")

        # Получаем текущий чеклист через родительский API
        from . import ChecklistAPI
        checklist_api = ChecklistAPI(self.client)
        current_checklist = await checklist_api.get(issue_id)

        # Находим обновляемый пункт
        item_to_update = None
        updated_checklist = []

        for item in current_checklist:
            if item['id'] == item_id:
                item_to_update = item.copy()
                # Обновляем поля
                item_to_update['text'] = text

                if checked is not None:
                    item_to_update['checked'] = checked

                # Обработка assignee
                if assignee is not None:
                    if isinstance(assignee, str):
                        # Определяем логин или ID по содержимому
                        if assignee.isdigit():
                            item_to_update['assignee'] = assignee  # ID как строка
                        else:
                            item_to_update['assignee'] = assignee  # Логин как строка
                    elif isinstance(assignee, int):
                        item_to_update['assignee'] = str(assignee)  # ID как строка
                    elif isinstance(assignee, dict):
                        # Объект с логином или ID
                        if 'login' in assignee:
                            item_to_update['assignee'] = assignee['login']
                        elif 'id' in assignee:
                            item_to_update['assignee'] = str(assignee['id'])
                        else:
                            raise ValueError("assignee объект должен содержать 'login' или 'id'")
                    else:
                        raise ValueError("assignee должен быть строкой, числом или объектом")
                elif assignee is None and 'assignee' in item_to_update:
                    # Убираем исполнителя
                    del item_to_update['assignee']

                # Обработка deadline
                if deadline is not None:
                    item_to_update['deadline'] = deadline
                elif deadline is None and 'deadline' in item_to_update:
                    # Убираем дедлайн
                    del item_to_update['deadline']

                updated_checklist.append(item_to_update)
            else:
                # Добавляем остальные пункты без изменений
                item_copy = item.copy()
                # Убираем служебные поля, которые не нужны для обновления
                for field in ['textHtml', 'checklistItemType']:
                    if field in item_copy:
                        del item_copy[field]
                updated_checklist.append(item_copy)

        if item_to_update is None:
            raise ValueError(f"Пункт чеклиста с ID '{item_id}' не найден")

        endpoint = f"/issues/{issue_id}/checklistItems/{item_id}"

        self.logger.info(f"Обновление пункта {item_id} чеклиста для задачи: {issue_id}")
        self.logger.debug(f"Новый текст: {text}")

        if checked is not None:
            status = "выполнен" if checked else "не выполнен"
            self.logger.debug(f"Новый статус: {status}")

        if assignee is not None:
            self.logger.debug(f"Новый исполнитель: {assignee}")
        elif assignee is None:
            self.logger.debug("Исполнитель убран")

        if deadline is not None:
            self.logger.debug(f"Новый дедлайн: {deadline['date']}")
        elif deadline is None:
            self.logger.debug("Дедлайн убран")

        try:
            # API требует передать все пункты чеклиста
            result = await self._request(endpoint, method='PUT', data=updated_checklist)

            # Логируем успешное обновление
            self.logger.info(f"Пункт {item_id} чеклиста успешно обновлен для задачи {issue_id}")

            if isinstance(result, list):
                updated_items_count = len(result)
                self.logger.debug(f"Получен обновленный чеклист с {updated_items_count} пунктами")

                # Находим и логируем обновленный пункт
                updated_item = next((item for item in result if item['id'] == item_id), None)
                if updated_item:
                    self.logger.debug(f"Обновленный пункт: '{updated_item['text']}' (статус: {'выполнен' if updated_item.get('checked', False) else 'не выполнен'})")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при обновлении пункта {item_id} чеклиста для задачи {issue_id}: {e}")
            raise

    async def delete(self, issue_id: str, item_id: str) -> Dict[str, Any]:
        """
        Удаление конкретного пункта чеклиста

        Удаляет указанный пункт из чеклиста задачи по его идентификатору.

        Args:
            issue_id: Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')
            item_id: Идентификатор пункта чеклиста для удаления

        Returns:
            Dict: Ответ от API об успешном удалении

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404, 400, 403)
            ValueError: При некорректных параметрах

        Examples:
            # Удаление конкретного пункта
            result = await client.issues.checklists.item.delete('TASK-123', 'item_id_123')
            print("Пункт чеклиста удален")

            # Поиск и удаление пункта по тексту
            checklist = await client.issues.checklists.get('TASK-123')
            target_text = 'Устаревший пункт'

            item_to_delete = next(
                (item for item in checklist if target_text in item['text']),
                None
            )

            if item_to_delete:
                await client.issues.checklists.item.delete('TASK-123', item_to_delete['id'])
                print(f"Удален пункт: {item_to_delete['text']}")
            else:
                print("Пункт для удаления не найден")

            # Удаление выполненных пунктов
            checklist = await client.issues.checklists.get('TASK-123')
            completed_items = [item for item in checklist if item['checked']]

            for item in completed_items:
                await client.issues.checklists.item.delete('TASK-123', item['id'])
                print(f"Удален выполненный пункт: {item['text']}")

            # Удаление пунктов с истекшими дедлайнами
            from datetime import datetime
            current_time = datetime.now()

            checklist = await client.issues.checklists.get('TASK-123')

            for item in checklist:
                if 'deadline' in item:
                    deadline_str = item['deadline']['date']
                    # Упрощенная проверка - в реальности нужен парсинг даты
                    if '2024-' in deadline_str:  # Пример для 2024 года
                        await client.issues.checklists.item.delete('TASK-123', item['id'])
                        print(f"Удален просроченный пункт: {item['text']}")

            # Обработка ошибок при удалении
            try:
                await client.issues.checklists.item.delete('TASK-123', 'non_existent_id')
            except Exception as e:
                print(f"Пункт не найден или уже удален: {e}")

            # Пакетное удаление по списку ID
            item_ids_to_delete = ['id1', 'id2', 'id3']

            for item_id in item_ids_to_delete:
                try:
                    await client.issues.checklists.item.delete('TASK-123', item_id)
                    print(f"Пункт {item_id} удален")
                except Exception as e:
                    print(f"Ошибка при удалении {item_id}: {e}")
        """

        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        if not item_id or not isinstance(item_id, str):
            raise ValueError("item_id должен быть непустой строкой")

        # Получаем информацию о пункте для логирования (если возможно)
        item_text = "неизвестный"
        try:
            from . import ChecklistAPI
            checklist_api = ChecklistAPI(self.client)
            current_checklist = await checklist_api.get(issue_id)
            target_item = next((item for item in current_checklist if item['id'] == item_id), None)
            if target_item:
                item_text = target_item['text']
        except Exception:
            pass  # Продолжаем удаление даже если не удается получить информацию

        endpoint = f"/issues/{issue_id}/checklistItems/{item_id}"

        self.logger.info(f"Удаление пункта {item_id} чеклиста для задачи: {issue_id}")
        if item_text != "неизвестный":
            self.logger.debug(f"Удаляемый пункт: '{item_text}'")

        try:
            result = await self._request(endpoint, method='DELETE')

            # Логируем успешное удаление
            self.logger.info(f"Пункт {item_id} чеклиста успешно удален для задачи {issue_id}")
            if item_text != "неизвестный":
                self.logger.debug(f"Удален пункт: '{item_text}'")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при удалении пункта {item_id} чеклиста для задачи {issue_id}: {e}")
            raise