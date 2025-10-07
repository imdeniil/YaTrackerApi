"""
API модуль для работы с переходами по жизненному циклу задач в Yandex Tracker
"""

from typing import Dict, Any, Optional, List
from ..base import BaseAPI


class TransitionsAPI(BaseAPI):
    """API для работы с переходами по жизненному циклу задач в Yandex Tracker"""

    async def get(self, issue_id: str) -> List[Dict[str, Any]]:
        """
        Получение доступных переходов для задачи

        Возвращает список всех доступных переходов по жизненному циклу для указанной задачи.
        Переходы определяются настройками воркфлоу и текущим статусом задачи.

        Args:
            issue_id: Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')

        Returns:
            List[Dict]: Список доступных переходов с их характеристиками

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404, 400, 403)
            ValueError: При некорректных параметрах

        Examples:
            # Получение всех доступных переходов
            transitions = await client.issues.transitions.get('TASK-123')

            # Анализ доступных переходов
            for transition in transitions:
                trans_id = transition['id']
                display_name = transition['display']
                to_status = transition['to']['display']
                print(f"Переход '{display_name}' -> {to_status} (ID: {trans_id})")

            # Поиск конкретного перехода
            close_transition = next(
                (t for t in transitions if 'close' in t['display'].lower()),
                None
            )

            if close_transition:
                print(f"Доступен переход к закрытию: {close_transition['display']}")

            # Группировка переходов по целевому статусу
            by_status = {}
            for transition in transitions:
                target_status = transition['to']['key']
                if target_status not in by_status:
                    by_status[target_status] = []
                by_status[target_status].append(transition)

            # Фильтрация переходов
            progress_transitions = [
                t for t in transitions
                if any(keyword in t['display'].lower()
                       for keyword in ['start', 'progress', 'begin'])
            ]

            # Результат содержит полную информацию о переходах
            print(f"Доступно {len(transitions)} переходов для задачи {issue_id}")
        """

        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        endpoint = f"/issues/{issue_id}/transitions"

        self.logger.info(f"Получение доступных переходов для задачи: {issue_id}")

        try:
            result = await self._request(endpoint, method='GET')

            # Логгируем результат
            transitions_count = len(result) if isinstance(result, list) else 0
            self.logger.info(f"Получено {transitions_count} доступных переходов для задачи {issue_id}")

            if transitions_count > 0:
                # Анализируем переходы для логирования
                target_statuses = set()
                for transition in result:
                    to_status = transition.get('to', {}).get('key')
                    if to_status:
                        target_statuses.add(to_status)

                self.logger.debug(f"Целевые статусы: {', '.join(target_statuses)}")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при получении переходов для задачи {issue_id}: {e}")
            raise

    async def update(
        self,
        issue_id: str,
        transition_id: str,
        comment: Optional[str] = None,
        **fields
    ) -> Dict[str, Any]:
        """
        Выполнение перехода по жизненному циклу задачи

        Выполняет указанный переход для задачи с возможностью добавления комментария
        и обновления полей задачи в рамках одной операции.

        Args:
            issue_id: Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')
            transition_id: Идентификатор перехода (получается из метода get())
            comment: Комментарий к переходу (необязательно)
            **fields: Дополнительные поля для обновления:
                - assignee: Новый исполнитель задачи
                - resolution: Резолюция (для переходов к закрытию)
                - priority: Новый приоритет
                - localfields: Кастомные поля пользователя (Dict[str, Any])
                - И любые другие поля задачи

        Returns:
            Dict: Обновленная информация о задаче после перехода

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404, 400, 403)
            ValueError: При некорректных параметрах

        Examples:
            # Простой переход без дополнительных параметров
            result = await client.issues.transitions.update('TASK-123', 'transition_id')

            # Переход с комментарием
            result = await client.issues.transitions.update(
                'TASK-123',
                'close_transition_id',
                comment="Задача выполнена успешно"
            )

            # Переход с обновлением полей
            result = await client.issues.transitions.update(
                'TASK-123',
                'resolve_transition_id',
                comment="Исправлено в версии 1.2.3",
                assignee="tester",
                resolution="fixed"
            )

            # Переход с кастомными полями
            result = await client.issues.transitions.update(
                'TASK-123',
                'transition_id',
                comment="Переход с метриками",
                resolution="completed",
                localfields={
                    "completionTime": "2.5h",
                    "quality": "excellent",
                    "performanceScore": 95
                }
            )

            # Получение ID перехода из списка доступных
            transitions = await client.issues.transitions.get('TASK-123')
            close_transition = next(
                (t for t in transitions if 'close' in t['display'].lower()),
                None
            )

            if close_transition:
                result = await client.issues.transitions.update(
                    'TASK-123',
                    close_transition['id'],
                    comment="Автоматическое закрытие"
                )

            # Новый статус после перехода
            new_status = result['status']['display']
            print(f"Задача {issue_id} переведена в статус: {new_status}")
        """

        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        if not transition_id or not isinstance(transition_id, str):
            raise ValueError("transition_id должен быть непустой строкой")

        if comment is not None and not isinstance(comment, str):
            raise ValueError("comment должен быть строкой")

        # Извлекаем localfields из fields, если они есть
        localfields = fields.pop('localfields', None)
        if localfields is not None and not isinstance(localfields, dict):
            raise ValueError("localfields должен быть словарем")

        endpoint = f"/issues/{issue_id}/transitions/{transition_id}/_execute"

        # Подготавливаем payload
        payload = {}

        # Добавляем комментарий если указан
        if comment:
            payload['comment'] = comment

        # Добавляем обычные поля
        payload.update(fields)

        # Добавляем кастомные поля если указаны
        if localfields:
            payload.update(localfields)

        self.logger.info(f"Выполнение перехода {transition_id} для задачи: {issue_id}")
        if comment:
            self.logger.debug(f"Комментарий к переходу: {comment}")
        if fields:
            self.logger.debug(f"Обновляемые поля: {list(fields.keys())}")
        if localfields:
            self.logger.debug(f"Кастомные поля: {list(localfields.keys())}")

        try:
            result = await self._request(endpoint, method='POST', data=payload)

            # Логгируем успешный переход
            if isinstance(result, dict):
                # Если API вернул объект задачи
                new_status = result.get('status', {}).get('display', 'N/A')
                assignee = result.get('assignee', {}).get('display', 'N/A')
                self.logger.info(f"Переход успешно выполнен для задачи {issue_id}")
                self.logger.info(f"Новый статус: {new_status}, исполнитель: {assignee}")
            elif isinstance(result, list):
                # Если API вернул список (например, доступные переходы)
                self.logger.info(f"Переход успешно выполнен для задачи {issue_id}")
                if result:
                    # Если в списке есть информация о целевом статусе
                    target_status = result[0].get('to', {}).get('display', 'N/A')
                    self.logger.info(f"Целевой статус: {target_status}")
                self.logger.debug(f"API вернул список с {len(result)} элементами")
            else:
                self.logger.info(f"Переход успешно выполнен для задачи {issue_id}")
                self.logger.debug(f"Неожиданный тип ответа: {type(result)}")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при выполнении перехода {transition_id} для задачи {issue_id}: {e}")
            raise