"""
API модуль для работы с тегами очередей в Yandex Tracker
"""

from typing import List
from ..base import BaseAPI


class TagsAPI(BaseAPI):
    """API для работы с тегами очередей"""

    async def get(self, queue_id: str) -> List[str]:
        """
        Получение списка тегов очереди

        Args:
            queue_id: Идентификатор или ключ очереди

        Returns:
            List[str] со списком тегов

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404 если очередь не найдена)

        Examples:
            # Получение списка тегов очереди
            tags = await client.queues.tags.get('TREK')
        """

        endpoint = f"/queues/{queue_id}/tags"

        self.logger.debug(f"Получение списка тегов очереди {queue_id}")

        try:
            result = await self._request(endpoint, method='GET')
            self.logger.info(f"Список тегов очереди {queue_id} успешно получен")
            return result

        except Exception as e:
            self.logger.error(f"Ошибка при получении списка тегов очереди {queue_id}: {e}")
            raise

    async def delete(self, queue_id: str, tag: str) -> None:
        """
        Удаление тега из очереди

        Args:
            queue_id: Идентификатор или ключ очереди
            tag: Название тега для удаления

        Returns:
            None (при успешном удалении возвращается статус 204)

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Examples:
            # Удаление тега из очереди
            await client.queues.tags.delete('TREK', 'deprecated')
        """

        endpoint = f"/queues/{queue_id}/tags/_remove"

        # Формируем payload
        payload = {'tag': tag}

        self.logger.debug(f"Удаление тега {tag} из очереди {queue_id}")

        try:
            await self._request(endpoint, method='POST', data=payload)
            self.logger.info(f"Тег {tag} успешно удален из очереди {queue_id}")

        except Exception as e:
            self.logger.error(f"Ошибка при удалении тега {tag} из очереди {queue_id}: {e}")
            raise
