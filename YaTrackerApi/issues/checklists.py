"""
API модуль для работы с чеклистами задач в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class ChecklistAPI(BaseAPI):
    """API для работы с чеклистами задач в Yandex Tracker"""

    @property
    def item(self):
        """API для работы с отдельными пунктами чеклистов"""
        if not hasattr(self, '_item'):
            from .checklist_item import ChecklistItemAPI
            self._item = ChecklistItemAPI(self.client)
        return self._item

    async def get(self, issue_id: str) -> List[Dict[str, Any]]:
        """
        Получение всех пунктов чеклиста задачи

        Возвращает список всех пунктов чеклиста для указанной задачи
        с полной информацией о каждом пункте.

        Args:
            issue_id: Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')

        Returns:
            List[Dict]: Список пунктов чеклиста с их свойствами:
            - id: уникальный идентификатор пункта
            - text: текст пункта
            - textHtml: HTML-форматированный текст
            - checked: статус выполнения (True/False)
            - checklistItemType: тип пункта ('standard')
            - assignee: исполнитель (если назначен)
            - deadline: дедлайн (если установлен)

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404, 400, 403)
            ValueError: При некорректных параметрах

        Examples:
            # Получение всех пунктов чеклиста
            checklist = await client.issues.checklists.get('TASK-123')

            # Анализ пунктов чеклиста
            for item in checklist:
                item_id = item['id']
                text = item['text']
                is_checked = item['checked']
                status = "✅" if is_checked else "❌"
                print(f"{status} {text} (ID: {item_id})")

            # Подсчет статистики
            total_items = len(checklist)
            completed_items = sum(1 for item in checklist if item['checked'])
            progress = (completed_items / total_items * 100) if total_items > 0 else 0
            print(f"Прогресс: {completed_items}/{total_items} ({progress:.1f}%)")

            # Фильтрация невыполненных пунктов
            pending_items = [item for item in checklist if not item['checked']]
            print(f"Осталось выполнить: {len(pending_items)} пунктов")

            # Поиск пунктов с исполнителями
            assigned_items = [item for item in checklist if 'assignee' in item]
            for item in assigned_items:
                assignee_name = item['assignee']['display']
                print(f"Пункт '{item['text']}' назначен на {assignee_name}")

            # Поиск пунктов с дедлайнами
            items_with_deadlines = [item for item in checklist if 'deadline' in item]
            for item in items_with_deadlines:
                deadline_date = item['deadline']['date']
                print(f"Пункт '{item['text']}' с дедлайном: {deadline_date}")

            # Группировка по статусу
            completed = [item for item in checklist if item['checked']]
            pending = [item for item in checklist if not item['checked']]
            print(f"Выполнено: {len(completed)}, Ожидается: {len(pending)}")

            # Результат содержит полную информацию о чеклисте
            print(f"Чеклист содержит {len(checklist)} пунктов")
        """

        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        endpoint = f"/issues/{issue_id}/checklistItems"

        self.logger.info(f"Получение чеклиста для задачи: {issue_id}")

        try:
            result = await self._request(endpoint, method='GET')

            # Проверяем, что получили список
            if not isinstance(result, list):
                self.logger.warning(f"Неожиданный тип ответа: {type(result)}")
                result = []

            items_count = len(result)
            self.logger.info(f"Получено {items_count} пунктов чеклиста для задачи {issue_id}")

            if items_count > 0:
                # Анализируем чеклист для логирования
                completed_count = sum(1 for item in result if item.get('checked', False))
                progress = (completed_count / items_count * 100) if items_count > 0 else 0

                self.logger.debug(f"Статистика чеклиста: {completed_count}/{items_count} выполнено ({progress:.1f}%)")

                # Логируем пункты с исполнителями
                assigned_items = [item for item in result if 'assignee' in item]
                if assigned_items:
                    self.logger.debug(f"Пунктов с исполнителями: {len(assigned_items)}")

                # Логируем пункты с дедлайнами
                deadline_items = [item for item in result if 'deadline' in item]
                if deadline_items:
                    self.logger.debug(f"Пунктов с дедлайнами: {len(deadline_items)}")

                # Логируем типы пунктов
                item_types = set(item.get('checklistItemType', 'unknown') for item in result)
                self.logger.debug(f"Типы пунктов: {', '.join(item_types)}")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при получении чеклиста для задачи {issue_id}: {e}")
            raise

    async def create(
        self,
        issue_id: str,
        text: str,
        checked: Optional[bool] = None,
        assignee: Optional[Union[str, int, Dict[str, Union[str, int]]]] = None,
        deadline: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Создание пункта чеклиста для задачи

        Создает новый пункт чеклиста в указанной задаче с возможностью
        установки исполнителя, статуса выполнения и дедлайна.

        Args:
            issue_id: Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')
            text: Текст пункта чеклиста (обязательный параметр)
            checked: Отметка о выполнении пункта:
                - True: пункт отмечен как выполненный
                - False: пункт не отмечен как выполненный
                - None (по умолчанию): не устанавливается
            assignee: Исполнитель пункта чеклиста:
                - Строка: логин пользователя
                - Число: ID пользователя
                - Объект: {"login": "username"} или {"id": "123"}
                - None (по умолчанию): не назначается
            deadline: Дедлайн пункта чеклиста:
                - {"date": "2021-05-09T00:00:00.000+0000", "deadlineType": "date"}
                - None (по умолчанию): без дедлайна

        Returns:
            Dict: Информация о созданном пункте чеклиста

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404, 400, 403)
            ValueError: При некорректных параметрах

        Examples:
            # Простое создание пункта чеклиста
            item = await client.issues.checklists.create(
                'TASK-123',
                'Проверить документацию'
            )

            # Создание с исполнителем
            item = await client.issues.checklists.create(
                'TASK-123',
                'Провести код-ревью',
                assignee='reviewer1'
            )

            # Создание выполненного пункта
            item = await client.issues.checklists.create(
                'TASK-123',
                'Написать unit тесты',
                checked=True,
                assignee={'login': 'developer'}
            )

            # Создание с дедлайном
            item = await client.issues.checklists.create(
                'TASK-123',
                'Деплой в продакшн',
                assignee='devops-team',
                deadline={
                    'date': '2025-12-31T23:59:59.000+0000',
                    'deadlineType': 'date'
                }
            )

            # Полный пример с все параметрами
            item = await client.issues.checklists.create(
                'PROJ-456',
                'Финальная проверка перед релизом',
                checked=False,
                assignee={'id': '1234567890'},
                deadline={
                    'date': '2025-10-15T18:00:00.000+0000',
                    'deadlineType': 'date'
                }
            )

            # Результат содержит информацию о созданном пункте
            print(f"Создан пункт: {item['text']}")
            print(f"ID пункта: {item['id']}")
            if 'assignee' in item:
                print(f"Исполнитель: {item['assignee']['display']}")
        """

        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        if not text or not isinstance(text, str):
            raise ValueError("text должен быть непустой строкой")

        if checked is not None and not isinstance(checked, bool):
            raise ValueError("checked должен быть логическим значением")

        if deadline is not None:
            if not isinstance(deadline, dict):
                raise ValueError("deadline должен быть словарем")
            if 'date' not in deadline or 'deadlineType' not in deadline:
                raise ValueError("deadline должен содержать поля 'date' и 'deadlineType'")

        endpoint = f"/issues/{issue_id}/checklistItems"

        # Строим payload
        payload = {
            'text': text
        }

        # Добавляем опциональные параметры
        if checked is not None:
            payload['checked'] = checked

        if assignee is not None:
            if isinstance(assignee, str):
                # Определяем логин или ID по содержимому
                if assignee.isdigit():
                    payload['assignee'] = assignee  # ID как строка
                else:
                    payload['assignee'] = assignee  # Логин как строка
            elif isinstance(assignee, int):
                payload['assignee'] = str(assignee)  # ID как строка
            elif isinstance(assignee, dict):
                # Объект с логином или ID
                if 'login' in assignee:
                    payload['assignee'] = assignee['login']
                elif 'id' in assignee:
                    payload['assignee'] = str(assignee['id'])
                else:
                    raise ValueError("assignee объект должен содержать 'login' или 'id'")
            else:
                raise ValueError("assignee должен быть строкой, числом или объектом")

        if deadline is not None:
            payload['deadline'] = deadline

        self.logger.info(f"Создание пункта чеклиста для задачи: {issue_id}")
        self.logger.debug(f"Текст пункта: {text}")

        if checked is not None:
            status = "выполнен" if checked else "не выполнен"
            self.logger.debug(f"Статус пункта: {status}")

        if assignee is not None:
            self.logger.debug(f"Исполнитель: {assignee}")

        if deadline is not None:
            self.logger.debug(f"Дедлайн: {deadline['date']}")

        try:
            result = await self._request(endpoint, method='POST', data=payload)

            # Логгируем успешное создание
            created_id = result.get('id', 'N/A')
            created_text = result.get('text', text)

            self.logger.info(f"Пункт чеклиста успешно создан для задачи {issue_id}")
            self.logger.debug(f"ID пункта: {created_id}, текст: '{created_text}'")

            if 'assignee' in result:
                assignee_name = result['assignee'].get('display', 'N/A')
                self.logger.debug(f"Назначенный исполнитель: {assignee_name}")

            if 'deadline' in result:
                deadline_date = result['deadline'].get('date', 'N/A')
                self.logger.debug(f"Установлен дедлайн: {deadline_date}")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при создании пункта чеклиста для задачи {issue_id}: {e}")
            raise


    async def delete(self, issue_id: str) -> Dict[str, Any]:
        """
        Удаление всех пунктов чеклиста задачи

        Полностью очищает чеклист указанной задачи, удаляя все пункты.

        Args:
            issue_id: Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')

        Returns:
            Dict: Ответ от API об успешном удалении

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404, 400, 403)
            ValueError: При некорректных параметрах

        Examples:
            # Полная очистка чеклиста
            result = await client.issues.checklists.delete('TASK-123')
            print("Чеклист полностью очищен")

            # Проверка результата
            if result:
                print("Все пункты чеклиста успешно удалены")

            # Получение пустого чеклиста после удаления
            empty_checklist = await client.issues.checklists.get('TASK-123')
            print(f"Пунктов в чеклисте: {len(empty_checklist)}")  # Должно быть 0

            # Использование в процессе очистки задачи
            try:
                await client.issues.checklists.delete('TASK-123')
                print("Чеклист очищен перед архивированием задачи")
            except Exception as e:
                print(f"Ошибка при очистке чеклиста: {e}")

            # Массовая очистка чеклистов
            task_ids = ['TASK-1', 'TASK-2', 'TASK-3']
            for task_id in task_ids:
                try:
                    await client.issues.checklists.delete(task_id)
                    print(f"Чеклист задачи {task_id} очищен")
                except Exception as e:
                    print(f"Ошибка при очистке чеклиста {task_id}: {e}")
        """

        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        # Сначала получаем информацию о текущем чеклисте для логирования
        try:
            current_checklist = await self.get(issue_id)
            items_count = len(current_checklist)
        except Exception:
            items_count = 0  # Если не удается получить, продолжаем

        endpoint = f"/issues/{issue_id}/checklistItems"

        self.logger.info(f"Удаление всех пунктов чеклиста для задачи: {issue_id}")
        if items_count > 0:
            self.logger.debug(f"Будет удалено {items_count} пунктов")

        try:
            result = await self._request(endpoint, method='DELETE')

            # Логируем успешное удаление
            self.logger.info(f"Все пункты чеклиста успешно удалены для задачи {issue_id}")
            if items_count > 0:
                self.logger.debug(f"Удалено {items_count} пунктов чеклиста")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при удалении всех пунктов чеклиста для задачи {issue_id}: {e}")
            raise

