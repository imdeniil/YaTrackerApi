"""
API модуль для работы с внешними связями (remote links) в Yandex Tracker
"""

from typing import Dict, Any, Optional, List
from ..base import BaseAPI


class ExternalLinksAPI(BaseAPI):
    """API для работы с внешними приложениями и связями"""

    async def get_applications(self) -> List[Dict[str, Any]]:
        """
        Получить список внешних приложений

        Returns:
            Список приложений, доступных для создания связей
        """
        self.logger.debug("Получение списка внешних приложений")
        result = await self._request('/applications')
        self.logger.info(f"Получено приложений: {len(result) if isinstance(result, list) else '?'}")
        return result

    async def list(self, issue_id: str) -> List[Dict[str, Any]]:
        """
        Получить список внешних связей задачи

        Args:
            issue_id: Ключ или ID задачи
        """
        endpoint = f"/issues/{issue_id}/remotelinks"
        self.logger.debug(f"Получение внешних связей задачи {issue_id}")
        result = await self._request(endpoint)
        self.logger.info(f"Получено связей: {len(result) if isinstance(result, list) else '?'}")
        return result

    async def create(
        self,
        issue_id: str,
        relationship: str,
        key: str,
        origin: str,
        backlink: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Добавить внешнюю связь

        Args:
            issue_id: Ключ или ID задачи
            relationship: Тип связи (рекомендуется 'RELATES')
            key: Ключ объекта во внешнем приложении
            origin: Идентификатор внешнего приложения
            backlink: Если True, Трекер отправит запрос на создание
                      обратной связи во внешнее приложение
        """
        endpoint = f"/issues/{issue_id}/remotelinks"

        params = None
        if backlink is not None:
            params = {"backlink": str(backlink).lower()}

        payload = {
            "relationship": relationship,
            "key": key,
            "origin": origin
        }

        self.logger.debug(f"Добавление внешней связи к задаче {issue_id}")
        result = await self._request(endpoint, method='POST', data=payload, params=params)
        self.logger.info(f"Внешняя связь добавлена к задаче {issue_id}")
        return result

    async def delete(self, issue_id: str, remotelink_id: int) -> Dict[str, Any]:
        """
        Удалить внешнюю связь

        Args:
            issue_id: Ключ или ID задачи
            remotelink_id: ID внешней связи
        """
        endpoint = f"/issues/{issue_id}/remotelinks/{remotelink_id}"

        self.logger.debug(f"Удаление внешней связи {remotelink_id} из задачи {issue_id}")
        result = await self._request(endpoint, method='DELETE')
        self.logger.info(f"Внешняя связь {remotelink_id} удалена из задачи {issue_id}")
        return result
