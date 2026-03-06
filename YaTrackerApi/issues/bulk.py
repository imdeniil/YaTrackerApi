"""
API модуль для пакетных операций с задачами в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class BulkAPI(BaseAPI):
    """API для пакетных операций с задачами в Yandex Tracker"""

    async def move(
        self,
        queue: str,
        issues: List[str],
        values: Optional[Dict[str, Any]] = None,
        move_all_fields: Optional[bool] = None,
        initial_status: Optional[bool] = None,
        notify: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Массовый перенос задач в другую очередь.

        Args:
            queue: Ключ целевой очереди
            issues: Список ключей задач для переноса
            values: Значения полей для установки после переноса
            move_all_fields: Перенести версии/компоненты/проекты если они есть в новой очереди
            initial_status: Сбросить статус задач на начальный
            notify: Уведомить пользователей (по умолчанию false)

        Returns:
            Dict: Информация о созданной пакетной операции (id, status)
        """
        if not queue or not isinstance(queue, str):
            raise ValueError("queue должен быть непустой строкой")
        if not issues or not isinstance(issues, list):
            raise ValueError("issues должен быть непустым списком")

        payload: Dict[str, Any] = {'queue': queue, 'issues': issues}
        if values is not None:
            payload['values'] = values
        if move_all_fields is not None:
            payload['moveAllFields'] = move_all_fields
        if initial_status is not None:
            payload['initialStatus'] = initial_status

        params = {}
        if notify is not None:
            params['notify'] = str(notify).lower()

        return await self._request(
            '/bulkchange/_move', method='POST', data=payload,
            params=params or None
        )

    async def update(
        self,
        issues: Union[List[str], str],
        values: Dict[str, Any],
        notify: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Массовое редактирование задач.

        Args:
            issues: Список ключей задач или строка YQL-фильтра
            values: Поля для обновления. Поддерживает операторы: set, add, remove, replace
            notify: Уведомить пользователей (по умолчанию false)

        Returns:
            Dict: Информация о созданной пакетной операции
        """
        if not issues:
            raise ValueError("issues не может быть пустым")
        if not values or not isinstance(values, dict):
            raise ValueError("values должен быть непустым словарём")

        payload: Dict[str, Any] = {'issues': issues, 'values': values}

        params = {}
        if notify is not None:
            params['notify'] = str(notify).lower()

        return await self._request(
            '/bulkchange/_update', method='POST', data=payload,
            params=params or None
        )

    async def transition(
        self,
        transition: str,
        issues: List[str],
        values: Optional[Dict[str, Any]] = None,
        notify: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Массовое изменение статуса задач.

        Args:
            transition: ID перехода (например, 'start_progress', 'close')
            issues: Список ключей задач
            values: Дополнительные поля (например, resolution при закрытии)
            notify: Уведомить пользователей (по умолчанию false)

        Returns:
            Dict: Информация о созданной пакетной операции
        """
        if not transition or not isinstance(transition, str):
            raise ValueError("transition должен быть непустой строкой")
        if not issues or not isinstance(issues, list):
            raise ValueError("issues должен быть непустым списком")

        payload: Dict[str, Any] = {'transition': transition, 'issues': issues}
        if values is not None:
            payload['values'] = values

        params = {}
        if notify is not None:
            params['notify'] = str(notify).lower()

        return await self._request(
            '/bulkchange/_transition', method='POST', data=payload,
            params=params or None
        )

    async def get_status(self, bulk_change_id: str) -> Dict[str, Any]:
        """
        Получить информацию о выполнении пакетной операции.

        Args:
            bulk_change_id: ID пакетной операции

        Returns:
            Dict: Статус операции (id, status, statusText, executionIssuePercent, totalIssues и др.)
        """
        if not bulk_change_id or not isinstance(bulk_change_id, str):
            raise ValueError("bulk_change_id должен быть непустой строкой")

        return await self._request(f'/bulkchange/{bulk_change_id}')

    async def get_failed_issues(self, bulk_change_id: str) -> List[Dict[str, Any]]:
        """
        Получить список задач, для которых пакетная операция завершилась ошибкой.

        Args:
            bulk_change_id: ID пакетной операции

        Returns:
            List[Dict]: Список задач с ошибками (issue, status, statusText, error)
        """
        if not bulk_change_id or not isinstance(bulk_change_id, str):
            raise ValueError("bulk_change_id должен быть непустой строкой")

        return await self._request(f'/bulkchange/{bulk_change_id}/issues')
