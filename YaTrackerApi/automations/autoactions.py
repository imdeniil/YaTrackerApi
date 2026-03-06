"""
API модуль для работы с автодействиями (Autoactions) в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class AutoactionsAPI(BaseAPI):
    """API для работы с автодействиями очередей"""

    async def create(
        self,
        queue: str,
        name: str,
        actions: List[Dict[str, Any]],
        filter: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        query: Optional[str] = None,
        active: Optional[bool] = None,
        enable_notifications: Optional[bool] = None,
        interval_millis: Optional[int] = None,
        calendar: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Создать автодействие

        Args:
            queue: Идентификатор или ключ очереди
            name: Название автодействия
            actions: Действия для выполнения над задачами
            filter: Условия фильтрации задач (альтернатива query)
            query: Строка запроса для фильтрации задач (альтернатива filter)
            active: Статус автодействия (true — активно)
            enable_notifications: Отправлять ли уведомления
            interval_millis: Интервал запуска в миллисекундах (по умолчанию 3600000)
            calendar: Период активности автодействия ({"id": <schedule_id>})

        Returns:
            Dict с параметрами созданного автодействия
        """
        endpoint = f"/queues/{queue}/autoactions"

        payload: Dict[str, Any] = {
            "name": name,
            "actions": actions
        }

        if filter is not None:
            payload["filter"] = filter
        if query is not None:
            payload["query"] = query
        if active is not None:
            payload["active"] = active
        if enable_notifications is not None:
            payload["enableNotifications"] = enable_notifications
        if interval_millis is not None:
            payload["intervalMillis"] = interval_millis
        if calendar is not None:
            payload["calendar"] = calendar

        self.logger.debug(f"Создание автодействия '{name}' в очереди {queue}")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info(f"Автодействие '{name}' успешно создано в очереди {queue}")
        return result

    async def get(
        self,
        queue: str,
        autoaction_id: Union[str, int]
    ) -> Dict[str, Any]:
        """
        Получить параметры автодействия

        Args:
            queue: Идентификатор или ключ очереди
            autoaction_id: Идентификатор автодействия

        Returns:
            Dict с параметрами автодействия
        """
        endpoint = f"/queues/{queue}/autoactions/{autoaction_id}"

        self.logger.debug(f"Получение автодействия {autoaction_id} из очереди {queue}")
        result = await self._request(endpoint, method='GET')
        self.logger.info(f"Автодействие {autoaction_id} успешно получено")
        return result

    async def get_logs(
        self,
        queue: str,
        autoaction_id: Union[str, int],
        launch_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Просмотреть логи автодействия

        Args:
            queue: Идентификатор или ключ очереди
            autoaction_id: Идентификатор автодействия
            launch_id: Идентификатор конкретного запуска (если не указан — все запуски)

        Returns:
            List с записями логов
        """
        if launch_id:
            endpoint = f"/queues/{queue}/autoactions/{autoaction_id}/logs/{launch_id}"
        else:
            endpoint = f"/queues/{queue}/autoactions/{autoaction_id}/logs"

        self.logger.debug(f"Получение логов автодействия {autoaction_id} из очереди {queue}")
        result = await self._request(endpoint, method='GET')
        self.logger.info(f"Логи автодействия {autoaction_id} успешно получены")
        return result
