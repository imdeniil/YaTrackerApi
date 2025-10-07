"""
API модуль для работы с полями очередей в Yandex Tracker
"""

from typing import Dict, Any, List
from ..base import BaseAPI


class FieldsAPI(BaseAPI):
    """API для работы с полями очередей"""

    async def get(self, queue_id: str) -> List[Dict[str, Any]]:
        """
        Получение списка полей очереди

        Args:
            queue_id: Идентификатор или ключ очереди

        Returns:
            List[Dict] со списком полей очереди

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404 если очередь не найдена)

        Examples:
            # Получение списка полей очереди
            fields = await client.queues.fields.get('TREK')
        """

        endpoint = f"/queues/{queue_id}/fields"

        self.logger.debug(f"Получение списка полей очереди {queue_id}")

        try:
            result = await self._request(endpoint, method='GET')
            self.logger.info(f"Список полей очереди {queue_id} успешно получен")
            return result

        except Exception as e:
            self.logger.error(f"Ошибка при получении списка полей очереди {queue_id}: {e}")
            raise
