from typing import List, Dict, Any, Union, Optional
from ..base import BaseAPI


class FiltersAPI(BaseAPI):
    """API для работы с фильтрами в Yandex Tracker

    Важно: Фильтры используют API v2 (/v2/filters/),
    в отличие от остальных модулей, работающих с v3.
    """

    async def _request(self, endpoint: str, method: str = 'GET',
                      data: Optional[Dict] = None,
                      params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Переопределение _request для использования v2 API.
        Подменяет base_url с /v3 на /v2 для запросов к фильтрам.
        """
        original_base_url = self.client.base_url
        self.client.base_url = original_base_url.replace('/v3', '/v2')
        try:
            return await self.client.request(endpoint, method, data, params)
        finally:
            self.client.base_url = original_base_url

    async def create(
        self,
        name: str,
        filter: Optional[Dict[str, Any]] = None,
        query: Optional[str] = None,
        fields: Optional[List[str]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        group_by: Optional[str] = None,
        folder: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Создать фильтр.

        Args:
            name: Название фильтра (обязательный)
            filter: Параметры фильтрации задач (несовместим с query)
            query: Язык запросов для фильтрации (несовместим с filter)
            fields: Список полей задачи для отображения
            sorts: Список параметров сортировки [{field, isAscending}]
            group_by: Поле для группировки задач
            folder: ID папки для размещения фильтра

        Returns:
            Dict с параметрами созданного фильтра

        Raises:
            ValueError: Если указаны одновременно filter и query
            aiohttp.ClientResponseError: При ошибках HTTP запроса
        """
        if filter is not None and query is not None:
            raise ValueError("Параметры 'filter' и 'query' взаимоисключающие. Укажите только один из них.")

        payload: Dict[str, Any] = {'name': name}
        if filter is not None:
            payload['filter'] = filter
        if query is not None:
            payload['query'] = query
        if fields is not None:
            payload['fields'] = fields
        if sorts is not None:
            payload['sorts'] = sorts
        if group_by is not None:
            payload['groupBy'] = group_by
        if folder is not None:
            payload['folder'] = folder

        return await self._request('/filters/', method='POST', data=payload)

    async def get(self, filter_id: int) -> Dict[str, Any]:
        """
        Получить параметры фильтра.

        Args:
            filter_id: ID фильтра (число)

        Returns:
            Dict с параметрами фильтра

        Raises:
            ValueError: Если filter_id не является положительным числом
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если фильтр не найден
        """
        if not isinstance(filter_id, int) or filter_id <= 0:
            raise ValueError(f"filter_id должен быть положительным целым числом, получено: {filter_id}")

        return await self._request(f'/filters/{filter_id}')

    async def update(
        self,
        filter_id: int,
        name: Optional[str] = None,
        filter: Optional[Dict[str, Any]] = None,
        query: Optional[str] = None,
        fields: Optional[List[str]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        group_by: Optional[str] = None,
        folder: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Редактировать фильтр.

        Важно: параметр filter полностью заменяет предыдущее значение,
        а не обновляет частично.

        Args:
            filter_id: ID фильтра (число)
            name: Новое название фильтра
            filter: Новые параметры фильтрации (полная замена, несовместим с query)
            query: Новый язык запросов (несовместим с filter)
            fields: Новый список полей задачи для отображения
            sorts: Новый список параметров сортировки [{field, isAscending}]
            group_by: Новое поле для группировки задач
            folder: Новый ID папки для размещения фильтра

        Returns:
            Dict с обновлёнными параметрами фильтра

        Raises:
            ValueError: Если filter_id некорректен или указаны оба filter и query
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если фильтр не найден
        """
        if not isinstance(filter_id, int) or filter_id <= 0:
            raise ValueError(f"filter_id должен быть положительным целым числом, получено: {filter_id}")

        if filter is not None and query is not None:
            raise ValueError("Параметры 'filter' и 'query' взаимоисключающие. Укажите только один из них.")

        payload: Dict[str, Any] = {}
        if name is not None:
            payload['name'] = name
        if filter is not None:
            payload['filter'] = filter
        if query is not None:
            payload['query'] = query
        if fields is not None:
            payload['fields'] = fields
        if sorts is not None:
            payload['sorts'] = sorts
        if group_by is not None:
            payload['groupBy'] = group_by
        if folder is not None:
            payload['folder'] = folder

        return await self._request(f'/filters/{filter_id}', method='PATCH', data=payload)
