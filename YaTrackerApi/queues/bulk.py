"""
API модуль для массового управления доступом к очередям в Yandex Tracker
"""

from typing import Dict, Any, Optional, List
from ..base import BaseAPI


class BulkAPI(BaseAPI):
    """API для массового управления доступом к очередям"""

    async def update(
        self,
        queue_id: str,
        # Опциональные параметры для управления правами
        create: Optional[Dict[str, List[str]]] = None,
        write: Optional[Dict[str, List[str]]] = None,
        read: Optional[Dict[str, List[str]]] = None,
        grant: Optional[Dict[str, List[str]]] = None
    ) -> Dict[str, Any]:
        """
        Массовое изменение доступа к очереди

        Args:
            queue_id: Идентификатор или ключ очереди
            create: Права на создание задач (add/remove списки пользователей/групп/ролей)
            write: Права на редактирование задач (add/remove списки пользователей/групп/ролей)
            read: Права на чтение задач (add/remove списки пользователей/групп/ролей)
            grant: Права на изменение настроек очереди (add/remove списки пользователей/групп/ролей)

        Returns:
            Dict с информацией об обновленных правах доступа

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Examples:
            # Добавление прав на создание и удаление прав на редактирование
            result = await client.queues.bulk.update(
                queue_id='TREK',
                create={'add': ['user1', 'user2']},
                write={'remove': ['user3']}
            )
        """

        endpoint = f"/queues/{queue_id}/permissions"

        # Формируем payload
        payload = {}

        if create is not None:
            payload['create'] = create
        if write is not None:
            payload['write'] = write
        if read is not None:
            payload['read'] = read
        if grant is not None:
            payload['grant'] = grant

        self.logger.debug(f"Массовое обновление прав доступа к очереди {queue_id}")

        try:
            result = await self._request(endpoint, method='PATCH', data=payload)
            self.logger.info(f"Права доступа к очереди {queue_id} успешно обновлены")
            return result

        except Exception as e:
            self.logger.error(f"Ошибка при обновлении прав доступа к очереди {queue_id}: {e}")
            raise
