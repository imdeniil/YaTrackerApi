"""
API модуль для работы с прикреплёнными файлами задач в Yandex Tracker
"""

from typing import Dict, Any, Optional, List, Union
from ..base import BaseAPI


class AttachmentsAPI(BaseAPI):
    """API для работы с прикреплёнными файлами задач в Yandex Tracker"""

    async def list(self, issue_id: str) -> List[Dict[str, Any]]:
        """
        Получить список прикреплённых файлов задачи.

        Args:
            issue_id: Идентификатор или ключ задачи (например, 'TASK-123')

        Returns:
            List[Dict]: Список файлов с полями: id, name, content, thumbnail,
                        createdBy, createdAt, mimetype, size, metadata
        """
        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        endpoint = f"/issues/{issue_id}/attachments"
        return await self._request(endpoint, method='GET')

    async def download(self, issue_id: str, attachment_id: Union[str, int],
                       filename: str) -> bytes:
        """
        Скачать прикреплённый файл.

        Args:
            issue_id: Идентификатор или ключ задачи
            attachment_id: ID вложения
            filename: Имя файла

        Returns:
            bytes: Содержимое файла
        """
        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")
        if not filename or not isinstance(filename, str):
            raise ValueError("filename должен быть непустой строкой")

        endpoint = f"/issues/{issue_id}/attachments/{attachment_id}/{filename}"
        return await self.client.request_binary(endpoint)

    async def download_thumbnail(self, issue_id: str,
                                  attachment_id: Union[str, int]) -> bytes:
        """
        Скачать миниатюру прикреплённого файла.

        Args:
            issue_id: Идентификатор или ключ задачи
            attachment_id: ID вложения

        Returns:
            bytes: Содержимое миниатюры (изображение)
        """
        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        endpoint = f"/issues/{issue_id}/thumbnails/{attachment_id}"
        return await self.client.request_binary(endpoint)

    async def attach(self, issue_id: str, file_data: bytes, filename: str,
                     new_filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Прикрепить файл к задаче.

        Args:
            issue_id: Идентификатор или ключ задачи
            file_data: Содержимое файла (bytes)
            filename: Имя файла для multipart
            new_filename: Новое имя файла на сервере (опционально)

        Returns:
            Dict: Информация о прикреплённом файле
        """
        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")
        if not file_data:
            raise ValueError("file_data не может быть пустым")
        if not filename or not isinstance(filename, str):
            raise ValueError("filename должен быть непустой строкой")

        endpoint = f"/issues/{issue_id}/attachments/"
        params = {}
        if new_filename is not None:
            params['filename'] = new_filename

        return await self.client.request_multipart(
            endpoint, file_data, filename, params=params or None
        )

    async def upload_temp(self, file_data: bytes, filename: str,
                          new_filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Загрузить временный файл.

        Временный файл можно использовать однократно при создании задачи
        или комментария (через attachment_ids).

        Args:
            file_data: Содержимое файла (bytes)
            filename: Имя файла для multipart
            new_filename: Новое имя файла на сервере (опционально)

        Returns:
            Dict: Информация о загруженном временном файле (id для дальнейшего использования)
        """
        if not file_data:
            raise ValueError("file_data не может быть пустым")
        if not filename or not isinstance(filename, str):
            raise ValueError("filename должен быть непустой строкой")

        endpoint = "/attachments/"
        params = {}
        if new_filename is not None:
            params['filename'] = new_filename

        return await self.client.request_multipart(
            endpoint, file_data, filename, params=params or None
        )

    async def delete(self, issue_id: str,
                     attachment_id: Union[str, int]) -> Dict[str, Any]:
        """
        Удалить прикреплённый файл.

        Args:
            issue_id: Идентификатор или ключ задачи
            attachment_id: ID вложения

        Returns:
            Dict: Ответ от API (пустой при 204)
        """
        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        endpoint = f"/issues/{issue_id}/attachments/{attachment_id}"
        return await self._request(endpoint, method='DELETE')
