from typing import List, Dict, Any, Optional
from ..base import BaseAPI

EntityType = str


class EntityAttachmentsAPI(BaseAPI):
    """API для работы с прикреплёнными файлами сущностей (проекты, портфели, цели) в Yandex Tracker"""

    async def list(
        self,
        entity_type: EntityType,
        entity_id: str
    ) -> List[Dict[str, Any]]:
        """
        Получить список прикреплённых файлов сущности.

        Args:
            entity_type: Тип сущности (project, portfolio, goal)
            entity_id: Идентификатор сущности

        Returns:
            List[Dict[str, Any]]: Список файлов
        """
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        self.logger.info(f"Получение файлов сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/attachments'
        result = await self._request(endpoint, 'GET')

        files_count = len(result) if isinstance(result, list) else 0
        self.logger.info(f"Получено {files_count} файлов для сущности {entity_type} '{entity_id}'")
        return result

    async def get(
        self,
        entity_type: EntityType,
        entity_id: str,
        file_id: str
    ) -> Dict[str, Any]:
        """
        Получить информацию о прикреплённом файле.

        Args:
            entity_type: Тип сущности (project, portfolio, goal)
            entity_id: Идентификатор сущности
            file_id: Идентификатор файла

        Returns:
            Dict[str, Any]: Информация о файле
        """
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(file_id, str) or not file_id.strip():
            raise ValueError("file_id должен быть непустой строкой")

        self.logger.info(f"Получение файла {file_id} сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/attachments/{file_id}'
        result = await self._request(endpoint, 'GET')

        self.logger.info(f"Файл {file_id} успешно получен")
        return result

    async def attach(
        self,
        entity_type: EntityType,
        entity_id: str,
        file_id: str,
        notify: Optional[bool] = None,
        notify_author: Optional[bool] = None,
        fields: Optional[str] = None,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Прикрепить файл к сущности (файл должен быть предварительно загружен как временный).

        Args:
            entity_type: Тип сущности (project, portfolio, goal)
            entity_id: Идентификатор сущности
            file_id: Идентификатор временного файла
            notify: Уведомлять пользователей
            notify_author: Уведомлять автора изменений
            fields: Дополнительные поля сущности в ответе
            expand: Дополнительная информация (attachments)

        Returns:
            Dict[str, Any]: Информация о сущности с прикреплённым файлом
        """
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(file_id, str) or not file_id.strip():
            raise ValueError("file_id должен быть непустой строкой")

        self.logger.info(f"Прикрепление файла {file_id} к сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/attachments/{file_id}'

        params = {}
        if notify is not None:
            params['notify'] = 'true' if notify else 'false'
        if notify_author is not None:
            params['notifyAuthor'] = 'true' if notify_author else 'false'
        if fields is not None:
            params['fields'] = fields
        if expand is not None:
            params['expand'] = expand

        result = await self._request(endpoint, 'POST', params=params or None)

        self.logger.info(f"Файл {file_id} успешно прикреплён к сущности {entity_type} '{entity_id}'")
        return result

    async def delete(
        self,
        entity_type: EntityType,
        entity_id: str,
        file_id: str
    ) -> None:
        """
        Удалить прикреплённый файл сущности.

        Args:
            entity_type: Тип сущности (project, portfolio, goal)
            entity_id: Идентификатор сущности
            file_id: Идентификатор файла
        """
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(file_id, str) or not file_id.strip():
            raise ValueError("file_id должен быть непустой строкой")

        self.logger.info(f"Удаление файла {file_id} сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/attachments/{file_id}'
        await self._request(endpoint, 'DELETE')

        self.logger.info(f"Файл {file_id} успешно удалён")
