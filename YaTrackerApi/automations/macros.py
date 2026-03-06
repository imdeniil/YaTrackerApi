"""
API модуль для работы с макросами (Macros) в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class MacrosAPI(BaseAPI):
    """API для работы с макросами очередей"""

    async def list(
        self,
        queue: str
    ) -> List[Dict[str, Any]]:
        """
        Получить все макросы очереди

        Args:
            queue: Идентификатор или ключ очереди

        Returns:
            List с макросами очереди
        """
        endpoint = f"/queues/{queue}/macros"

        self.logger.debug(f"Получение макросов очереди {queue}")
        result = await self._request(endpoint, method='GET')
        self.logger.info(f"Макросы очереди {queue} успешно получены")
        return result

    async def get(
        self,
        queue: str,
        macro_id: Union[str, int]
    ) -> Dict[str, Any]:
        """
        Получить макрос

        Args:
            queue: Идентификатор или ключ очереди
            macro_id: Идентификатор макроса

        Returns:
            Dict с параметрами макроса
        """
        endpoint = f"/queues/{queue}/macros/{macro_id}"

        self.logger.debug(f"Получение макроса {macro_id} из очереди {queue}")
        result = await self._request(endpoint, method='GET')
        self.logger.info(f"Макрос {macro_id} успешно получен")
        return result

    async def create(
        self,
        queue: str,
        name: str,
        body: Optional[str] = None,
        issue_update: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Создать макрос

        Args:
            queue: Идентификатор или ключ очереди
            name: Название макроса
            body: Текст комментария при выполнении макроса
            issue_update: Поля задачи для обновления при выполнении

        Returns:
            Dict с параметрами созданного макроса
        """
        endpoint = f"/queues/{queue}/macros"

        payload: Dict[str, Any] = {"name": name}

        if body is not None:
            payload["body"] = body
        if issue_update is not None:
            payload["issueUpdate"] = issue_update

        self.logger.debug(f"Создание макроса '{name}' в очереди {queue}")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info(f"Макрос '{name}' успешно создан в очереди {queue}")
        return result

    async def update(
        self,
        queue: str,
        macro_id: Union[str, int],
        name: str,
        body: Optional[str] = None,
        issue_update: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Редактировать макрос

        Args:
            queue: Идентификатор или ключ очереди
            macro_id: Идентификатор макроса
            name: Название макроса (обязательное)
            body: Текст комментария при выполнении макроса
            issue_update: Поля задачи для обновления при выполнении

        Returns:
            Dict с обновленными параметрами макроса
        """
        endpoint = f"/queues/{queue}/macros/{macro_id}"

        payload: Dict[str, Any] = {"name": name}

        if body is not None:
            payload["body"] = body
        if issue_update is not None:
            payload["issueUpdate"] = issue_update

        self.logger.debug(f"Обновление макроса {macro_id} в очереди {queue}")
        result = await self._request(endpoint, method='PATCH', data=payload)
        self.logger.info(f"Макрос {macro_id} успешно обновлен")
        return result

    async def delete(
        self,
        queue: str,
        macro_id: Union[str, int]
    ) -> None:
        """
        Удалить макрос

        Args:
            queue: Идентификатор или ключ очереди
            macro_id: Идентификатор макроса

        Returns:
            None (при успешном удалении возвращается статус 204)
        """
        endpoint = f"/queues/{queue}/macros/{macro_id}"

        self.logger.debug(f"Удаление макроса {macro_id} из очереди {queue}")
        await self._request(endpoint, method='DELETE')
        self.logger.info(f"Макрос {macro_id} успешно удален")
