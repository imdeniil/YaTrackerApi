"""
API модуль для работы с учётом времени (Time Tracking) в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class WorklogAPI(BaseAPI):
    """API для работы с записями о затраченном времени"""

    async def create(
        self,
        issue_id: str,
        start: str,
        duration: str,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Добавить запись о затраченном времени

        Args:
            issue_id: Идентификатор или ключ задачи
            start: Дата/время начала (YYYY-MM-DDThh:mm:ss.sss±hhmm)
            duration: Затраченное время в формате ISO 8601 (PT1H30M, P5DT20M, P1W)
            comment: Комментарий к записи

        Returns:
            Dict с параметрами созданной записи
        """
        endpoint = f"/issues/{issue_id}/worklog"

        payload: Dict[str, Any] = {
            "start": start,
            "duration": duration
        }
        if comment is not None:
            payload["comment"] = comment

        self.logger.debug(f"Создание записи о времени для задачи {issue_id}")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info(f"Запись о времени для задачи {issue_id} успешно создана")
        return result

    async def list(
        self,
        issue_id: str,
        per_page: Optional[int] = None,
        id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить все записи по задаче

        Args:
            issue_id: Идентификатор или ключ задачи
            per_page: Количество записей на странице (макс 500)
            id: ID записи для курсорной пагинации

        Returns:
            List с записями о затраченном времени
        """
        endpoint = f"/issues/{issue_id}/worklog"

        params: Dict[str, Any] = {}
        if per_page is not None:
            params["perPage"] = per_page
        if id is not None:
            params["id"] = id

        self.logger.debug(f"Получение записей о времени для задачи {issue_id}")
        result = await self._request(endpoint, method='GET', params=params or None)
        self.logger.info(f"Записи о времени для задачи {issue_id} успешно получены")
        return result

    async def search(
        self,
        created_by: Optional[str] = None,
        created_at_from: Optional[str] = None,
        created_at_to: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Отобрать записи по параметрам (POST /worklog/_search)

        Args:
            created_by: Логин или ID автора
            created_at_from: Начало диапазона (YYYY-MM-DDThh:mm:ss.sss±hhmm)
            created_at_to: Конец диапазона (YYYY-MM-DDThh:mm:ss.sss±hhmm)

        Returns:
            List с записями о затраченном времени
        """
        endpoint = "/worklog/_search"

        payload: Dict[str, Any] = {}
        if created_by is not None:
            payload["createdBy"] = created_by
        if created_at_from is not None or created_at_to is not None:
            created_at: Dict[str, str] = {}
            if created_at_from is not None:
                created_at["from"] = created_at_from
            if created_at_to is not None:
                created_at["to"] = created_at_to
            payload["createdAt"] = created_at

        self.logger.debug("Поиск записей о времени")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info("Записи о времени успешно найдены")
        return result

    async def update(
        self,
        issue_id: str,
        worklog_id: Union[str, int],
        duration: str,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Редактировать запись о затраченном времени

        Args:
            issue_id: Идентификатор или ключ задачи
            worklog_id: Идентификатор записи
            duration: Новое затраченное время в формате ISO 8601
            comment: Новый комментарий

        Returns:
            Dict с обновленными параметрами записи
        """
        endpoint = f"/issues/{issue_id}/worklog/{worklog_id}"

        payload: Dict[str, Any] = {"duration": duration}
        if comment is not None:
            payload["comment"] = comment

        self.logger.debug(f"Обновление записи {worklog_id} для задачи {issue_id}")
        result = await self._request(endpoint, method='PATCH', data=payload)
        self.logger.info(f"Запись {worklog_id} для задачи {issue_id} успешно обновлена")
        return result

    async def delete(
        self,
        issue_id: str,
        worklog_id: Union[str, int]
    ) -> None:
        """
        Удалить запись о затраченном времени

        Args:
            issue_id: Идентификатор или ключ задачи
            worklog_id: Идентификатор записи
        """
        endpoint = f"/issues/{issue_id}/worklog/{worklog_id}"

        self.logger.debug(f"Удаление записи {worklog_id} для задачи {issue_id}")
        await self._request(endpoint, method='DELETE')
        self.logger.info(f"Запись {worklog_id} для задачи {issue_id} успешно удалена")
