"""
API модуль для работы с версиями очередей в Yandex Tracker
"""

from typing import Dict, Any, Optional, List
from ..base import BaseAPI


class VersionsAPI(BaseAPI):
    """API для работы с версиями очередей"""

    async def create(
        self,
        queue: str,
        name: str,
        # Опциональные параметры
        description: Optional[str] = None,
        start_date: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Создание версии в очереди

        Args:
            queue: Ключ очереди
            name: Название версии
            description: Описание версии
            start_date: Дата начала в формате YYYY-MM-DD
            due_date: Дата окончания в формате YYYY-MM-DD

        Returns:
            Dict с информацией о созданной версии

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Examples:
            # Создание версии
            version = await client.queues.versions.create(
                queue='TESTQUEUE',
                name='version 0.1',
                description='Test version 1',
                start_date='2023-10-03',
                due_date='2024-06-03'
            )
        """

        endpoint = "/versions/"

        # Формируем payload
        payload = {
            'queue': queue,
            'name': name
        }

        # Добавляем опциональные параметры
        if description is not None:
            payload['description'] = description
        if start_date is not None:
            payload['startDate'] = start_date
        if due_date is not None:
            payload['dueDate'] = due_date

        self.logger.debug(f"Создание версии {name} в очереди {queue}")

        try:
            result = await self._request(endpoint, method='POST', data=payload)
            self.logger.info(f"Версия {name} успешно создана в очереди {queue}")
            return result

        except Exception as e:
            self.logger.error(f"Ошибка при создании версии {name} в очереди {queue}: {e}")
            raise

    async def get(self, queue_id: str) -> List[Dict[str, Any]]:
        """
        Получение списка версий очереди

        Args:
            queue_id: Идентификатор или ключ очереди

        Returns:
            List[Dict] со списком версий очереди

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404 если очередь не найдена)

        Examples:
            # Получение списка версий очереди
            versions = await client.queues.versions.get('TREK')
        """

        endpoint = f"/queues/{queue_id}/versions"

        self.logger.debug(f"Получение списка версий очереди {queue_id}")

        try:
            result = await self._request(endpoint, method='GET')
            self.logger.info(f"Список версий очереди {queue_id} успешно получен")
            return result

        except Exception as e:
            self.logger.error(f"Ошибка при получении списка версий очереди {queue_id}: {e}")
            raise
