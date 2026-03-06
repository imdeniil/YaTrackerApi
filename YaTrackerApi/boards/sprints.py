"""
API модуль для работы со спринтами в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class SprintsAPI(BaseAPI):
    """API для работы со спринтами"""

    async def list(
        self,
        board_id: Union[str, int]
    ) -> List[Dict[str, Any]]:
        """
        Получить все спринты доски

        Args:
            board_id: Идентификатор доски

        Returns:
            List со спринтами доски
        """
        endpoint = f"/boards/{board_id}/sprints"

        self.logger.debug(f"Получение спринтов доски {board_id}")
        result = await self._request(endpoint, method='GET')
        self.logger.info(f"Спринты доски {board_id} успешно получены")
        return result

    async def get(
        self,
        sprint_id: Union[str, int]
    ) -> Dict[str, Any]:
        """
        Получить спринт

        Args:
            sprint_id: Идентификатор спринта

        Returns:
            Dict с параметрами спринта
        """
        endpoint = f"/sprints/{sprint_id}"

        self.logger.debug(f"Получение спринта {sprint_id}")
        result = await self._request(endpoint, method='GET')
        self.logger.info(f"Спринт {sprint_id} успешно получен")
        return result

    async def create(
        self,
        name: str,
        board_id: Union[str, int],
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """
        Создать спринт

        Args:
            name: Название спринта
            board_id: Идентификатор доски
            start_date: Дата начала (YYYY-MM-DD)
            end_date: Дата окончания (YYYY-MM-DD)

        Returns:
            Dict с параметрами созданного спринта
        """
        endpoint = "/sprints"

        payload = {
            "name": name,
            "board": {"id": str(board_id)},
            "startDate": start_date,
            "endDate": end_date
        }

        self.logger.debug(f"Создание спринта '{name}' для доски {board_id}")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info(f"Спринт '{name}' успешно создан")
        return result
