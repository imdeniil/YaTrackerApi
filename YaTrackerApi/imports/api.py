"""
API модуль для импорта данных в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class ImportsAPI(BaseAPI):
    """API для импорта задач, комментариев, связей и файлов"""

    async def issue(
        self,
        queue: str,
        summary: str,
        created_at: str,
        created_by: Union[str, int],
        key: Optional[str] = None,
        updated_at: Optional[str] = None,
        updated_by: Optional[Union[str, int]] = None,
        resolved_at: Optional[str] = None,
        resolved_by: Optional[Union[str, int]] = None,
        resolution: Optional[int] = None,
        status: Optional[int] = None,
        type: Optional[int] = None,
        deadline: Optional[str] = None,
        description: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        assignee: Optional[Union[str, int]] = None,
        priority: Optional[int] = None,
        affected_versions: Optional[List[int]] = None,
        fix_versions: Optional[List[int]] = None,
        components: Optional[List[int]] = None,
        tags: Optional[List[str]] = None,
        sprint: Optional[List[int]] = None,
        followers: Optional[List[Union[str, int]]] = None,
        access: Optional[List[Union[str, int]]] = None,
        unique: Optional[str] = None,
        original_estimation: Optional[int] = None,
        estimation: Optional[int] = None,
        spent: Optional[int] = None,
        story_points: Optional[float] = None,
        voted_by: Optional[List[Union[str, int]]] = None,
        favorited_by: Optional[List[Union[str, int]]] = None
    ) -> Dict[str, Any]:
        """
        Импортировать задачу

        Args:
            queue: Ключ очереди
            summary: Название задачи (макс 255 символов)
            created_at: Дата создания (YYYY-MM-DDThh:mm:ss.sss±hhmm)
            created_by: Логин или ID автора
            key: Ключ задачи (должен принадлежать очереди)
            updated_at: Дата изменения (используется вместе с updated_by)
            updated_by: Логин или ID последнего редактора
            resolved_at: Дата резолюции (вместе с resolution и resolved_by)
            resolved_by: Логин или ID решившего
            resolution: ID резолюции
            status: ID статуса
            type: ID типа задачи
            deadline: Дедлайн (YYYY-MM-DD)
            description: Описание (макс 512000 символов)
            start: Дата начала (YYYY-MM-DD)
            end: Дата окончания (YYYY-MM-DD)
            assignee: Логин или ID исполнителя
            priority: ID приоритета
            affected_versions: ID версий "Обнаружено в"
            fix_versions: ID версий "Исправлено в"
            components: ID компонентов
            tags: Теги
            sprint: ID спринтов
            followers: Наблюдатели
            access: Доступ
            unique: Уникальный внешний идентификатор
            original_estimation: Первоначальная оценка (мс)
            estimation: Оценка (мс)
            spent: Затрачено времени (мс)
            story_points: Story Points
            voted_by: Проголосовавшие
            favorited_by: Добавившие в избранное
        """
        endpoint = "/issues/_import"

        payload: Dict[str, Any] = {
            "queue": queue,
            "summary": summary,
            "createdAt": created_at,
            "createdBy": created_by
        }

        if key is not None:
            payload["key"] = key
        if updated_at is not None:
            payload["updatedAt"] = updated_at
        if updated_by is not None:
            payload["updatedBy"] = updated_by
        if resolved_at is not None:
            payload["resolvedAt"] = resolved_at
        if resolved_by is not None:
            payload["resolvedBy"] = resolved_by
        if resolution is not None:
            payload["resolution"] = resolution
        if status is not None:
            payload["status"] = status
        if type is not None:
            payload["type"] = type
        if deadline is not None:
            payload["deadline"] = deadline
        if description is not None:
            payload["description"] = description
        if start is not None:
            payload["start"] = start
        if end is not None:
            payload["end"] = end
        if assignee is not None:
            payload["assignee"] = assignee
        if priority is not None:
            payload["priority"] = priority
        if affected_versions is not None:
            payload["affectedVersions"] = affected_versions
        if fix_versions is not None:
            payload["fixVersions"] = fix_versions
        if components is not None:
            payload["components"] = components
        if tags is not None:
            payload["tags"] = tags
        if sprint is not None:
            payload["sprint"] = sprint
        if followers is not None:
            payload["followers"] = followers
        if access is not None:
            payload["access"] = access
        if unique is not None:
            payload["unique"] = unique
        if original_estimation is not None:
            payload["originalEstimation"] = original_estimation
        if estimation is not None:
            payload["estimation"] = estimation
        if spent is not None:
            payload["spent"] = spent
        if story_points is not None:
            payload["storyPoints"] = story_points
        if voted_by is not None:
            payload["votedBy"] = voted_by
        if favorited_by is not None:
            payload["favoritedBy"] = favorited_by

        self.logger.debug(f"Импорт задачи в очередь {queue}")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info(f"Задача успешно импортирована в очередь {queue}")
        return result

    async def comment(
        self,
        issue_id: str,
        text: str,
        created_at: str,
        created_by: Union[str, int],
        updated_at: Optional[str] = None,
        updated_by: Optional[Union[str, int]] = None
    ) -> Dict[str, Any]:
        """
        Импортировать комментарий

        Args:
            issue_id: Ключ задачи
            text: Текст комментария (макс 512000 символов)
            created_at: Дата создания (YYYY-MM-DDThh:mm:ss.sss±hhmm)
            created_by: Логин или ID автора
            updated_at: Дата изменения (вместе с updated_by)
            updated_by: Логин или ID редактора
        """
        endpoint = f"/issues/{issue_id}/comments/_import"

        payload: Dict[str, Any] = {
            "text": text,
            "createdAt": created_at,
            "createdBy": created_by
        }

        if updated_at is not None:
            payload["updatedAt"] = updated_at
        if updated_by is not None:
            payload["updatedBy"] = updated_by

        self.logger.debug(f"Импорт комментария в задачу {issue_id}")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info(f"Комментарий успешно импортирован в задачу {issue_id}")
        return result

    async def link(
        self,
        issue_id: str,
        relationship: str,
        issue: str,
        created_at: str,
        created_by: Union[str, int],
        updated_at: Optional[str] = None,
        updated_by: Optional[Union[str, int]] = None
    ) -> Dict[str, Any]:
        """
        Импортировать связь

        Args:
            issue_id: Ключ задачи, к которой добавляется связь
            relationship: Тип связи ('relates', 'is dependent by', 'depends on',
                'is subtask for', 'is parent task for', 'duplicates',
                'is duplicated by', 'is epic of', 'has epic', 'clone', 'original')
            issue: Ключ или ID связанной задачи
            created_at: Дата создания связи (YYYY-MM-DDThh:mm:ss.sss±hhmm)
            created_by: Логин или ID создателя связи
            updated_at: Дата изменения (вместе с updated_by)
            updated_by: Логин или ID редактора
        """
        endpoint = f"/issues/{issue_id}/links/_import"

        payload: Dict[str, Any] = {
            "relationship": relationship,
            "issue": issue,
            "createdAt": created_at,
            "createdBy": created_by
        }

        if updated_at is not None:
            payload["updatedAt"] = updated_at
        if updated_by is not None:
            payload["updatedBy"] = updated_by

        self.logger.debug(f"Импорт связи для задачи {issue_id}")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info(f"Связь успешно импортирована для задачи {issue_id}")
        return result

    async def file(
        self,
        issue_id: str,
        file_data: bytes,
        filename: str,
        created_at: str,
        created_by: str,
        comment_id: Optional[Union[str, int]] = None
    ) -> Dict[str, Any]:
        """
        Импортировать файл (к задаче или к комментарию)

        Args:
            issue_id: Ключ задачи
            file_data: Содержимое файла (bytes)
            filename: Имя файла (макс 255 символов)
            created_at: Дата прикрепления (YYYY-MM-DDThh:mm:ss.sss±hhmm)
            created_by: Логин или ID автора
            comment_id: ID комментария (если файл прикрепляется к комментарию)
        """
        if comment_id is not None:
            endpoint = f"/issues/{issue_id}/comments/{comment_id}/attachments/_import"
        else:
            endpoint = f"/issues/{issue_id}/attachments/_import"

        params = {
            "filename": filename,
            "createdAt": created_at,
            "createdBy": created_by
        }

        self.logger.debug(f"Импорт файла '{filename}' в задачу {issue_id}")
        result = await self.client.request_multipart(endpoint, file_data, filename, params=params)
        self.logger.info(f"Файл '{filename}' успешно импортирован в задачу {issue_id}")
        return result
