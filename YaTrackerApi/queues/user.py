"""
API модуль для получения доступа пользователя к очереди в Yandex Tracker
"""

from typing import Dict, Any
from ..base import BaseAPI


class UserAPI(BaseAPI):
    """API для получения доступа пользователя к очереди"""

    async def get(self, queue_id: str, user_id: str) -> Dict[str, Any]:
        """
        Получение прав доступа пользователя к очереди

        Args:
            queue_id: Идентификатор или ключ очереди
            user_id: Логин или ID пользователя

        Returns:
            Dict с информацией о правах доступа пользователя

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404 если очередь или пользователь не найдены)

        Examples:
            # Получение прав доступа пользователя к очереди
            access = await client.queues.user.get('TREK', 'username')
        """

        endpoint = f"/queues/{queue_id}/permissions/users/{user_id}"

        self.logger.debug(f"Получение прав доступа пользователя {user_id} к очереди {queue_id}")

        try:
            result = await self._request(endpoint, method='GET')
            self.logger.info(f"Права доступа пользователя {user_id} к очереди {queue_id} успешно получены")
            return result

        except Exception as e:
            self.logger.error(f"Ошибка при получении прав доступа пользователя {user_id} к очереди {queue_id}: {e}")
            raise
