"""
API модуль для получения доступа группы к очереди в Yandex Tracker
"""

from typing import Dict, Any
from ..base import BaseAPI


class GroupAPI(BaseAPI):
    """API для получения доступа группы к очереди"""

    async def get(self, queue_id: str, group_id: str) -> Dict[str, Any]:
        """
        Получение прав доступа группы к очереди

        Args:
            queue_id: Идентификатор или ключ очереди
            group_id: ID группы

        Returns:
            Dict с информацией о правах доступа группы

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404 если очередь или группа не найдены)

        Examples:
            # Получение прав доступа группы к очереди
            access = await client.queues.group.get('TREK', '123')
        """

        endpoint = f"/queues/{queue_id}/permissions/groups/{group_id}"

        self.logger.debug(f"Получение прав доступа группы {group_id} к очереди {queue_id}")

        try:
            result = await self._request(endpoint, method='GET')
            self.logger.info(f"Права доступа группы {group_id} к очереди {queue_id} успешно получены")
            return result

        except Exception as e:
            self.logger.error(f"Ошибка при получении прав доступа группы {group_id} к очереди {queue_id}: {e}")
            raise
