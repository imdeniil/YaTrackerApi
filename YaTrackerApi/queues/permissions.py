"""
API модуль для управления правами доступа к очередям в Yandex Tracker
"""

from typing import Dict, Any, Optional
from ..base import BaseAPI


class PermissionsAPI(BaseAPI):
    """API для управления правами доступа к очередям"""

    async def update(
        self,
        queue_id: str,
        create: Optional[Dict[str, Any]] = None,
        write: Optional[Dict[str, Any]] = None,
        read: Optional[Dict[str, Any]] = None,
        grant: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Массовое изменение доступа к очереди

        Args:
            queue_id: Идентификатор или ключ очереди
            create: Права на создание задач
            write: Права на редактирование задач
            read: Права на чтение задач
            grant: Права на изменение настроек очереди

            Формат каждого параметра прав:
                {
                    "users": {"add": ["uid1"], "remove": ["uid2"]},
                    "groups": {"add": ["gid1"]},
                    "roles": {"add": ["queue-lead"]}
                }
            Или для замены всего списка:
                {"users": ["uid1", "uid2"]}
        """
        endpoint = f"/queues/{queue_id}/permissions"

        payload = {}
        if create is not None:
            payload['create'] = create
        if write is not None:
            payload['write'] = write
        if read is not None:
            payload['read'] = read
        if grant is not None:
            payload['grant'] = grant

        self.logger.debug(f"Обновление прав доступа к очереди {queue_id}")
        result = await self._request(endpoint, method='PATCH', data=payload)
        self.logger.info(f"Права доступа к очереди {queue_id} обновлены")
        return result

    async def get_user(self, queue_id: str, user_id: str) -> Dict[str, Any]:
        """
        Получить права доступа пользователя к очереди

        Args:
            queue_id: Идентификатор или ключ очереди
            user_id: Логин или ID пользователя
        """
        endpoint = f"/queues/{queue_id}/permissions/users/{user_id}"
        self.logger.debug(f"Получение прав пользователя {user_id} к очереди {queue_id}")
        result = await self._request(endpoint)
        self.logger.info(f"Права пользователя {user_id} к очереди {queue_id} получены")
        return result

    async def get_group(self, queue_id: str, group_id: str) -> Dict[str, Any]:
        """
        Получить права доступа группы к очереди

        Args:
            queue_id: Идентификатор или ключ очереди
            group_id: ID группы
        """
        endpoint = f"/queues/{queue_id}/permissions/groups/{group_id}"
        self.logger.debug(f"Получение прав группы {group_id} к очереди {queue_id}")
        result = await self._request(endpoint)
        self.logger.info(f"Права группы {group_id} к очереди {queue_id} получены")
        return result
