"""
API модуль для работы с триггерами (Triggers) в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class TriggersAPI(BaseAPI):
    """API для работы с триггерами очередей"""

    async def create(
        self,
        queue: str,
        name: str,
        actions: List[Dict[str, Any]],
        conditions: Optional[List[Dict[str, Any]]] = None,
        active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Создать триггер

        Args:
            queue: Идентификатор или ключ очереди
            name: Название триггера
            actions: Действия триггера (объекты действий)
            conditions: Условия срабатывания триггера (объекты условий)
            active: Статус триггера (true — активен)

        Returns:
            Dict с параметрами созданного триггера
        """
        endpoint = f"/queues/{queue}/triggers"

        payload: Dict[str, Any] = {
            "name": name,
            "actions": actions
        }

        if conditions is not None:
            payload["conditions"] = conditions
        if active is not None:
            payload["active"] = active

        self.logger.debug(f"Создание триггера '{name}' в очереди {queue}")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info(f"Триггер '{name}' успешно создан в очереди {queue}")
        return result

    async def get(
        self,
        queue: str,
        trigger_id: Union[str, int]
    ) -> Dict[str, Any]:
        """
        Получить параметры триггера

        Args:
            queue: Идентификатор или ключ очереди
            trigger_id: Идентификатор триггера

        Returns:
            Dict с параметрами триггера
        """
        endpoint = f"/queues/{queue}/triggers/{trigger_id}"

        self.logger.debug(f"Получение триггера {trigger_id} из очереди {queue}")
        result = await self._request(endpoint, method='GET')
        self.logger.info(f"Триггер {trigger_id} успешно получен")
        return result

    async def update(
        self,
        queue: str,
        trigger_id: Union[str, int],
        version: Optional[int] = None,
        name: Optional[str] = None,
        actions: Optional[List[Dict[str, Any]]] = None,
        conditions: Optional[List[Dict[str, Any]]] = None,
        active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Изменить триггер

        Если version не указан, автоматически получает текущую версию триггера.

        Args:
            queue: Идентификатор или ключ очереди
            trigger_id: Идентификатор триггера
            version: Версия триггера для оптимистичной блокировки
            name: Новое название триггера
            actions: Новые действия триггера
            conditions: Новые условия срабатывания
            active: Статус триггера

        Returns:
            Dict с обновленными параметрами триггера
        """
        # Автоматически получаем версию, если не указана
        if version is None:
            current = await self.get(queue, trigger_id)
            version = current.get('version')

        endpoint = f"/queues/{queue}/triggers/{trigger_id}"

        payload: Dict[str, Any] = {}

        if name is not None:
            payload["name"] = name
        if actions is not None:
            payload["actions"] = actions
        if conditions is not None:
            payload["conditions"] = conditions
        if active is not None:
            payload["active"] = active

        params = {"version": version} if version is not None else None

        self.logger.debug(f"Обновление триггера {trigger_id} в очереди {queue}")
        result = await self._request(endpoint, method='PATCH', data=payload, params=params)
        self.logger.info(f"Триггер {trigger_id} успешно обновлен")
        return result

    async def get_logs(
        self,
        queue: str,
        trigger_id: Union[str, int],
        issue_id: Optional[str] = None,
        limit: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Просмотреть логи триггера (только для триггеров с действием Webhook)

        Args:
            queue: Идентификатор или ключ очереди
            trigger_id: Идентификатор триггера
            issue_id: Фильтр по задаче (например, 'DEV-123')
            limit: Количество записей (по умолчанию 10, макс 100)
            from_date: Начало временного диапазона (YYYY-MM-DDThh:mm:ss)
            to_date: Конец временного диапазона (YYYY-MM-DDThh:mm:ss)

        Returns:
            List с записями логов вебхуков
        """
        endpoint = f"/queues/{queue}/triggers/{trigger_id}/webhooks/log"

        params: Dict[str, Any] = {}
        if issue_id is not None:
            params["issueId"] = issue_id
        if limit is not None:
            params["limit"] = limit
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        self.logger.debug(f"Получение логов триггера {trigger_id} из очереди {queue}")
        result = await self._request(endpoint, method='GET', params=params or None)
        self.logger.info(f"Логи триггера {trigger_id} успешно получены")
        return result
