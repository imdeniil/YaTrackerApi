"""
API модуль для работы с пользователями в Yandex Tracker
"""

from typing import Dict, Any, Union, Optional, List
from ..base import BaseAPI


class UsersAPI(BaseAPI):
    """API для работы с пользователями в Yandex Tracker"""

    async def get_myself(self, expand: Optional[str] = None) -> Dict[str, Any]:
        """
        Получить информацию о текущем пользователе

        Args:
            expand: Доп. поля ('groups' — включить группы пользователя)
        """
        params = {}
        if expand is not None:
            params["expand"] = expand

        self.logger.debug("Получение информации о текущем пользователе")
        result = await self._request('/myself', params=params or None)
        self.logger.info(f"Текущий пользователь: {result.get('display', '?')}")
        return result

    async def get(
        self,
        user_id: Union[str, int],
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Получить информацию о заданном пользователе

        Args:
            user_id: Логин или uid пользователя.
                     Если логин состоит только из цифр, используйте
                     префикс 'login:' (например 'login:12345')
            expand: Доп. поля ('groups' — включить группы пользователя)
        """
        params = {}
        if expand is not None:
            params["expand"] = expand

        endpoint = f"/users/{user_id}"
        self.logger.debug(f"Получение информации о пользователе {user_id}")
        result = await self._request(endpoint, params=params or None)
        self.logger.info(f"Пользователь: {result.get('display', '?')}")
        return result

    async def list(
        self,
        per_page: Optional[int] = None,
        id: Optional[int] = None,
        email: Optional[str] = None,
        group: Optional[int] = None,
        expand: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить информацию о пользователях (лимит 10 000)

        Args:
            per_page: Количество на странице (1–100)
            id: uid для начала поиска
            email: Фильтр по email
            group: Фильтр по ID группы
            expand: Доп. поля ('groups' — включить группы)
        """
        params = {}
        if per_page is not None:
            params["perPage"] = per_page
        if id is not None:
            params["id"] = id
        if email is not None:
            params["email"] = email
        if group is not None:
            params["group"] = group
        if expand is not None:
            params["expand"] = expand

        self.logger.debug("Получение списка пользователей")
        result = await self._request('/users', params=params or None)
        self.logger.info(f"Получено пользователей: {len(result) if isinstance(result, list) else '?'}")
        return result

    async def get_paginated(
        self,
        per_page: Optional[int] = None,
        id: Optional[int] = None,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Получить пользователей с относительной пагинацией (без лимита 10 000)

        Args:
            per_page: Количество на странице (1–100)
            id: uid для начала (курсор — передайте uid последнего
                пользователя предыдущей страницы)
            expand: Доп. поля ('groups' — включить группы)

        Returns:
            Dict с ключами 'users' (список) и 'hasNext' (bool)
        """
        params = {}
        if per_page is not None:
            params["perPage"] = per_page
        if id is not None:
            params["id"] = id
        if expand is not None:
            params["expand"] = expand

        self.logger.debug("Получение пользователей с пагинацией")
        result = await self._request('/users/_relative', params=params or None)
        users = result.get('users', []) if isinstance(result, dict) else []
        has_next = result.get('hasNext', False) if isinstance(result, dict) else False
        self.logger.info(f"Получено пользователей: {len(users)}, hasNext={has_next}")
        return result
