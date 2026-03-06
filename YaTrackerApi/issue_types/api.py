"""
API модуль для работы с типами задач, статусами, резолюциями и приоритетами
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class IssueTypesAPI(BaseAPI):
    """API для работы с типами задач"""

    async def list(self) -> List[Dict[str, Any]]:
        """Получить список типов задач"""
        result = await self._request("/issuetypes", method='GET')
        return result

    async def create(
        self,
        key: str,
        name: Dict[str, str]
    ) -> Any:
        """
        Создать тип задачи

        Args:
            key: Ключ типа задачи
            name: Название {"ru": "...", "en": "..."}
        """
        payload = {"key": key, "name": name}
        result = await self._request("/issuetypes/", method='POST', data=payload)
        return result

    async def update(
        self,
        id_or_key: Union[str, int],
        version: Optional[int] = None,
        name: Optional[Dict[str, str]] = None
    ) -> Any:
        """
        Редактировать тип задачи

        Args:
            id_or_key: ID или ключ типа задачи
            version: Версия для оптимистичной блокировки
            name: Новое название {"ru": "...", "en": "..."}
        """
        endpoint = f"/issuetypes/{id_or_key}"
        params = {"version": version} if version is not None else None
        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        result = await self._request(endpoint, method='PATCH', data=payload, params=params)
        return result


class StatusesAPI(BaseAPI):
    """API для работы со статусами задач"""

    async def list(self) -> List[Dict[str, Any]]:
        """Получить список статусов"""
        result = await self._request("/statuses", method='GET')
        return result

    async def create(
        self,
        key: str,
        name: Dict[str, str],
        type: str
    ) -> Any:
        """
        Создать статус задачи

        Args:
            key: Ключ статуса (латинские буквы, начинается с маленькой)
            name: Название {"ru": "...", "en": "..."}
            type: Тип статуса: 'new', 'inProgress', 'paused', 'done', 'cancelled'
        """
        payload = {"key": key, "name": name, "type": type}
        result = await self._request("/statuses/", method='POST', data=payload)
        return result

    async def update(
        self,
        id_or_key: Union[str, int],
        version: Optional[int] = None,
        name: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        order: Optional[int] = None,
        type: Optional[str] = None
    ) -> Any:
        """
        Редактировать статус задачи

        Args:
            id_or_key: ID или ключ статуса
            version: Версия для оптимистичной блокировки
            name: Новое название {"ru": "...", "en": "..."}
            description: Описание статуса
            order: Вес для сортировки
            type: Тип статуса
        """
        endpoint = f"/statuses/{id_or_key}"
        params = {"version": version} if version is not None else None
        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if order is not None:
            payload["order"] = order
        if type is not None:
            payload["type"] = type
        result = await self._request(endpoint, method='PATCH', data=payload, params=params)
        return result


class ResolutionsAPI(BaseAPI):
    """API для работы с резолюциями"""

    async def list(self) -> List[Dict[str, Any]]:
        """Получить список резолюций"""
        result = await self._request("/resolutions", method='GET')
        return result

    async def create(
        self,
        key: str,
        name: Dict[str, str]
    ) -> Any:
        """
        Создать резолюцию

        Args:
            key: Ключ резолюции (латинские буквы, начинается с маленькой)
            name: Название {"ru": "...", "en": "..."}
        """
        payload = {"key": key, "name": name}
        result = await self._request("/resolutions/", method='POST', data=payload)
        return result

    async def update(
        self,
        id_or_key: Union[str, int],
        version: Optional[int] = None,
        name: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        order: Optional[int] = None
    ) -> Any:
        """
        Редактировать резолюцию

        Args:
            id_or_key: ID или ключ резолюции
            version: Версия для оптимистичной блокировки
            name: Новое название {"ru": "...", "en": "..."}
            description: Описание
            order: Вес для сортировки
        """
        endpoint = f"/resolutions/{id_or_key}"
        params = {"version": version} if version is not None else None
        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if order is not None:
            payload["order"] = order
        result = await self._request(endpoint, method='PATCH', data=payload, params=params)
        return result


class PrioritiesAPI(BaseAPI):
    """API для работы с приоритетами"""

    async def list(
        self,
        localized: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить список приоритетов

        Args:
            localized: true — имена на языке пользователя, false — на всех языках
        """
        params = {}
        if localized is not None:
            params["localized"] = str(localized).lower()
        result = await self._request("/priorities", method='GET', params=params or None)
        return result

    async def create(
        self,
        key: str,
        name: Dict[str, str],
        order: int,
        description: Optional[str] = None
    ) -> Any:
        """
        Создать приоритет

        Args:
            key: Ключ приоритета
            name: Название {"ru": "...", "en": "..."}
            order: Вес для сортировки
            description: Описание
        """
        payload: Dict[str, Any] = {"key": key, "name": name, "order": order}
        if description is not None:
            payload["description"] = description
        result = await self._request("/priorities/", method='POST', data=payload)
        return result

    async def update(
        self,
        id_or_key: Union[str, int],
        version: Optional[int] = None,
        name: Optional[Dict[str, str]] = None,
        description: Optional[str] = None
    ) -> Any:
        """
        Редактировать приоритет

        Args:
            id_or_key: ID или ключ приоритета
            version: Версия для оптимистичной блокировки
            name: Новое название {"ru": "...", "en": "..."}
            description: Описание
        """
        endpoint = f"/priorities/{id_or_key}"
        params = {"version": version} if version is not None else None
        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        result = await self._request(endpoint, method='PATCH', data=payload, params=params)
        return result
