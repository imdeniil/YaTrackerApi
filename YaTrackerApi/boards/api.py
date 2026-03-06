"""
API модуль для работы с досками задач в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class BoardsAPI(BaseAPI):
    """API для работы с досками задач"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._columns = None
        self._sprints = None

    @property
    def columns(self):
        """Доступ к API для работы с колонками"""
        if self._columns is None:
            from .columns import ColumnsAPI
            self._columns = ColumnsAPI(self.client)
        return self._columns

    @property
    def sprints(self):
        """Доступ к API для работы со спринтами"""
        if self._sprints is None:
            from .sprints import SprintsAPI
            self._sprints = SprintsAPI(self.client)
        return self._sprints

    async def list(self) -> List[Dict[str, Any]]:
        """
        Получить параметры всех досок

        Returns:
            List с досками
        """
        endpoint = "/boards"

        self.logger.debug("Получение всех досок")
        result = await self._request(endpoint, method='GET')
        self.logger.info("Доски успешно получены")
        return result

    async def list_paginated(
        self,
        per_page: Optional[int] = None,
        id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить параметры всех досок с поддержкой пагинации

        Args:
            per_page: Количество досок на странице (макс 500)
            id: ID доски, с которого начать следующую страницу (курсорная пагинация)

        Returns:
            List с досками
        """
        endpoint = "/boards/_paginate"

        params: Dict[str, Any] = {}
        if per_page is not None:
            params["perPage"] = per_page
        if id is not None:
            params["id"] = id

        self.logger.debug("Получение досок с пагинацией")
        result = await self._request(endpoint, method='GET', params=params or None)
        self.logger.info("Доски с пагинацией успешно получены")
        return result

    async def get(
        self,
        board_id: Union[str, int]
    ) -> Dict[str, Any]:
        """
        Получить параметры доски задач

        Args:
            board_id: Идентификатор доски

        Returns:
            Dict с параметрами доски
        """
        endpoint = f"/boards/{board_id}"

        self.logger.debug(f"Получение доски {board_id}")
        result = await self._request(endpoint, method='GET')
        self.logger.info(f"Доска {board_id} успешно получена")
        return result

    async def create(
        self,
        name: str,
        owner: Optional[Union[str, int]] = None,
        board_permissions_template: Optional[str] = None,
        backlog_available: Optional[bool] = None,
        sprints_available: Optional[bool] = None,
        columns: Optional[List[Dict[str, Any]]] = None,
        backlog_columns: Optional[List[Dict[str, Any]]] = None,
        non_parametrized_columns: Optional[List[Dict[str, Any]]] = None,
        auto_filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Создать доску

        Args:
            name: Название доски
            owner: Логин или UID владельца
            board_permissions_template: Права доступа ('private' или 'public')
            backlog_available: Включить бэклог
            sprints_available: Включить спринты
            columns: Колонки доски
            backlog_columns: Колонки бэклога
            non_parametrized_columns: Свободные колонки
            auto_filters: Автофильтры (addFilter, removeFilter)

        Returns:
            Dict с параметрами созданной доски
        """
        endpoint = "/liveBoards/"

        payload: Dict[str, Any] = {"name": name}

        if owner is not None:
            payload["owner"] = owner
        if board_permissions_template is not None:
            payload["boardPermissionsTemplate"] = board_permissions_template
        if backlog_available is not None:
            payload["backlogAvailable"] = backlog_available
        if sprints_available is not None:
            payload["sprintsAvailable"] = sprints_available
        if columns is not None:
            payload["columns"] = columns
        if backlog_columns is not None:
            payload["backlogColumns"] = backlog_columns
        if non_parametrized_columns is not None:
            payload["nonParametrizedColumns"] = non_parametrized_columns
        if auto_filters is not None:
            payload["autoFilters"] = auto_filters

        self.logger.debug(f"Создание доски '{name}'")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info(f"Доска '{name}' успешно создана")
        return result

    async def update(
        self,
        board_id: Union[str, int],
        name: Optional[str] = None,
        backlog_available: Optional[bool] = None,
        sprints_available: Optional[bool] = None,
        columns: Optional[List[Dict[str, Any]]] = None,
        backlog_columns: Optional[List[Dict[str, Any]]] = None,
        non_parametrized_columns: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Редактировать доску

        Args:
            board_id: Идентификатор доски
            name: Новое название доски
            backlog_available: Включить/выключить бэклог
            sprints_available: Включить/выключить спринты
            columns: Новые колонки доски
            backlog_columns: Новые колонки бэклога
            non_parametrized_columns: Новые свободные колонки

        Returns:
            Dict с обновленными параметрами доски
        """
        endpoint = f"/boards/{board_id}"

        payload: Dict[str, Any] = {}

        if name is not None:
            payload["name"] = name
        if backlog_available is not None:
            payload["backlogAvailable"] = backlog_available
        if sprints_available is not None:
            payload["sprintsAvailable"] = sprints_available
        if columns is not None:
            payload["columns"] = columns
        if backlog_columns is not None:
            payload["backlogColumns"] = backlog_columns
        if non_parametrized_columns is not None:
            payload["nonParametrizedColumns"] = non_parametrized_columns

        self.logger.debug(f"Обновление доски {board_id}")
        result = await self._request(endpoint, method='PATCH', data=payload)
        self.logger.info(f"Доска {board_id} успешно обновлена")
        return result

    async def delete(
        self,
        board_id: Union[str, int]
    ) -> None:
        """
        Удалить доску

        Args:
            board_id: Идентификатор доски
        """
        endpoint = f"/boards/{board_id}"

        self.logger.debug(f"Удаление доски {board_id}")
        await self._request(endpoint, method='DELETE')
        self.logger.info(f"Доска {board_id} успешно удалена")
