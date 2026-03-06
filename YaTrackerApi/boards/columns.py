"""
API модуль для работы с колонками досок в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class ColumnsAPI(BaseAPI):
    """API для работы с колонками досок"""

    async def list(
        self,
        board_id: Union[str, int]
    ) -> List[Dict[str, Any]]:
        """
        Получить параметры всех колонок доски

        Args:
            board_id: Идентификатор доски

        Returns:
            List с колонками доски
        """
        endpoint = f"/boards/{board_id}/columns"

        self.logger.debug(f"Получение колонок доски {board_id}")
        result = await self._request(endpoint, method='GET')
        self.logger.info(f"Колонки доски {board_id} успешно получены")
        return result

    async def get(
        self,
        board_id: Union[str, int],
        column_id: Union[str, int]
    ) -> Dict[str, Any]:
        """
        Получить параметры колонки

        Args:
            board_id: Идентификатор доски
            column_id: Идентификатор колонки

        Returns:
            Dict с параметрами колонки
        """
        endpoint = f"/boards/{board_id}/columns/{column_id}"

        self.logger.debug(f"Получение колонки {column_id} доски {board_id}")
        result = await self._request(endpoint, method='GET')
        self.logger.info(f"Колонка {column_id} успешно получена")
        return result

    async def create(
        self,
        board_id: Union[str, int],
        name: str,
        statuses: List[str],
        board_version: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Создать колонку

        Требует версию доски для оптимистичной блокировки (заголовок If-Match).
        Если board_version не указан, автоматически получает текущую версию.

        Args:
            board_id: Идентификатор доски
            name: Название колонки
            statuses: Список ключей статусов для колонки
            board_version: Версия доски для If-Match

        Returns:
            Dict с параметрами созданной колонки
        """
        if board_version is None:
            board = await self._get_board(board_id)
            board_version = board.get('version')

        endpoint = f"/boards/{board_id}/columns/"

        payload = {
            "name": name,
            "statuses": statuses
        }

        self.logger.debug(f"Создание колонки '{name}' на доске {board_id}")
        result = await self._request_with_if_match(
            endpoint, method='POST', data=payload, version=board_version
        )
        self.logger.info(f"Колонка '{name}' успешно создана на доске {board_id}")
        return result

    async def update(
        self,
        board_id: Union[str, int],
        column_id: Union[str, int],
        board_version: Optional[int] = None,
        name: Optional[str] = None,
        statuses: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Редактировать колонку

        Args:
            board_id: Идентификатор доски
            column_id: Идентификатор колонки
            board_version: Версия доски для If-Match
            name: Новое название колонки
            statuses: Новый список ключей статусов

        Returns:
            Dict с обновленными параметрами колонки
        """
        if board_version is None:
            board = await self._get_board(board_id)
            board_version = board.get('version')

        endpoint = f"/boards/{board_id}/columns/{column_id}"

        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if statuses is not None:
            payload["statuses"] = statuses

        self.logger.debug(f"Обновление колонки {column_id} на доске {board_id}")
        result = await self._request_with_if_match(
            endpoint, method='PATCH', data=payload, version=board_version
        )
        self.logger.info(f"Колонка {column_id} успешно обновлена")
        return result

    async def delete(
        self,
        board_id: Union[str, int],
        column_id: Union[str, int],
        board_version: Optional[int] = None
    ) -> None:
        """
        Удалить колонку

        Args:
            board_id: Идентификатор доски
            column_id: Идентификатор колонки
            board_version: Версия доски для If-Match
        """
        if board_version is None:
            board = await self._get_board(board_id)
            board_version = board.get('version')

        endpoint = f"/boards/{board_id}/columns/{column_id}"

        self.logger.debug(f"Удаление колонки {column_id} с доски {board_id}")
        await self._request_with_if_match(
            endpoint, method='DELETE', version=board_version
        )
        self.logger.info(f"Колонка {column_id} успешно удалена")

    async def _get_board(self, board_id: Union[str, int]) -> Dict[str, Any]:
        """Получить данные доски для извлечения версии"""
        endpoint = f"/boards/{board_id}"
        return await self._request(endpoint, method='GET')

    async def _request_with_if_match(
        self,
        endpoint: str,
        method: str,
        version: int,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Any:
        """Выполнить запрос с заголовком If-Match"""
        import aiohttp

        url = f"{self.client.base_url}{endpoint}"

        kwargs: Dict[str, Any] = {
            'method': method,
            'url': url,
            'params': params,
            'headers': {'If-Match': f'"{version}"'}
        }

        if data is not None:
            kwargs['json'] = data

        async with self.client.session.request(**kwargs) as response:
            if response.status >= 400:
                error_text = await response.text()
                self.logger.error(f"HTTP ошибка {response.status}: {error_text}")
                response.raise_for_status()

            if response.status == 204:
                return None

            import json
            text = await response.text()
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {"raw_response": text}
