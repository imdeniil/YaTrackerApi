"""
API модуль для работы с правами доступа к компонентам в Yandex Tracker
"""

from typing import Dict, Any, Union
from ..base import BaseAPI


class ComponentPermissionsAPI(BaseAPI):
    """API для работы с правами доступа к компонентам"""

    async def get_user(
        self,
        component_id: Union[str, int],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Получить информацию о правах доступа пользователя к компоненту

        Args:
            component_id: Идентификатор компонента
            user_id: Логин или ID пользователя

        Returns:
            Dict с правами доступа пользователя
        """
        endpoint = f"/components/{component_id}/permissions/users/{user_id}"

        self.logger.debug(f"Получение прав пользователя {user_id} к компоненту {component_id}")
        result = await self._request(endpoint, method='GET')
        self.logger.info(f"Права пользователя {user_id} успешно получены")
        return result

    async def get_group(
        self,
        component_id: Union[str, int],
        group_id: Union[str, int]
    ) -> Dict[str, Any]:
        """
        Получить информацию о правах доступа группы к компоненту

        Args:
            component_id: Идентификатор компонента
            group_id: Идентификатор группы

        Returns:
            Dict с правами доступа группы
        """
        endpoint = f"/components/{component_id}/permissions/groups/{group_id}"

        self.logger.debug(f"Получение прав группы {group_id} к компоненту {component_id}")
        result = await self._request(endpoint, method='GET')
        self.logger.info(f"Права группы {group_id} успешно получены")
        return result
