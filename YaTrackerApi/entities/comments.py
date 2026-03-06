from typing import List, Dict, Any, Optional
from ..base import BaseAPI

EntityType = str


class EntityCommentsAPI(BaseAPI):
    """API для работы с комментариями сущностей (проекты, портфели, цели) в Yandex Tracker"""

    async def create(
        self,
        entity_type: EntityType,
        entity_id: str,
        text: str,
        attachment_ids: Optional[List[str]] = None,
        summonees: Optional[List] = None,
        maillist_summonees: Optional[List[str]] = None,
        is_add_to_followers: Optional[bool] = None,
        notify: Optional[bool] = None,
        notify_author: Optional[bool] = None,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Добавить комментарий к сущности.

        Args:
            entity_type: Тип сущности (project, portfolio, goal)
            entity_id: Идентификатор сущности
            text: Текст комментария (обязательное поле)
            attachment_ids: Список ID вложений
            summonees: Список призываемых пользователей (строки или объекты)
            maillist_summonees: Список рассылок для призыва
            is_add_to_followers: Добавить автора в наблюдатели
            notify: Уведомлять пользователей
            notify_author: Уведомлять автора изменений
            expand: Дополнительная информация (all, html, attachments, reactions)

        Returns:
            Dict[str, Any]: Созданный комментарий
        """
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(text, str) or not text.strip():
            raise ValueError("text должен быть непустой строкой")

        self.logger.info(f"Добавление комментария к сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/comments'

        params = {}
        if is_add_to_followers is not None:
            params['isAddToFollowers'] = 'true' if is_add_to_followers else 'false'
        if notify is not None:
            params['notify'] = 'true' if notify else 'false'
        if notify_author is not None:
            params['notifyAuthor'] = 'true' if notify_author else 'false'
        if expand is not None:
            params['expand'] = expand

        payload = {"text": text}
        if attachment_ids is not None:
            payload["attachmentIds"] = attachment_ids
        if summonees is not None:
            payload["summonees"] = summonees
        if maillist_summonees is not None:
            payload["maillistSummonees"] = maillist_summonees

        result = await self._request(endpoint, 'POST', data=payload, params=params or None)

        self.logger.info(f"Комментарий успешно добавлен к сущности {entity_type} '{entity_id}'")
        return result

    async def list(
        self,
        entity_type: EntityType,
        entity_id: str,
        expand: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить все комментарии к сущности.

        Args:
            entity_type: Тип сущности (project, portfolio, goal)
            entity_id: Идентификатор сущности
            expand: Дополнительная информация (all, html, attachments, reactions)

        Returns:
            List[Dict[str, Any]]: Список комментариев
        """
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        self.logger.info(f"Получение комментариев к сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/comments'

        params = {}
        if expand is not None:
            params['expand'] = expand

        result = await self._request(endpoint, 'GET', params=params or None)

        comments_count = len(result) if isinstance(result, list) else 0
        self.logger.info(f"Получено {comments_count} комментариев для сущности {entity_type} '{entity_id}'")
        return result

    async def get(
        self,
        entity_type: EntityType,
        entity_id: str,
        comment_id: str,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Получить конкретный комментарий сущности.

        Args:
            entity_type: Тип сущности (project, portfolio, goal)
            entity_id: Идентификатор сущности
            comment_id: Идентификатор комментария
            expand: Дополнительная информация (all, html, attachments, reactions)

        Returns:
            Dict[str, Any]: Комментарий
        """
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(comment_id, str) or not comment_id.strip():
            raise ValueError("comment_id должен быть непустой строкой")

        self.logger.info(f"Получение комментария {comment_id} сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/comments/{comment_id}'

        params = {}
        if expand is not None:
            params['expand'] = expand

        result = await self._request(endpoint, 'GET', params=params or None)

        self.logger.info(f"Комментарий {comment_id} успешно получен")
        return result

    async def update(
        self,
        entity_type: EntityType,
        entity_id: str,
        comment_id: str,
        text: Optional[str] = None,
        attachment_ids: Optional[List[str]] = None,
        summonees: Optional[List] = None,
        maillist_summonees: Optional[List[str]] = None,
        is_add_to_followers: Optional[bool] = None,
        notify: Optional[bool] = None,
        notify_author: Optional[bool] = None,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Редактировать комментарий сущности.

        Args:
            entity_type: Тип сущности (project, portfolio, goal)
            entity_id: Идентификатор сущности
            comment_id: Идентификатор комментария
            text: Новый текст комментария
            attachment_ids: Список ID вложений
            summonees: Список призываемых пользователей
            maillist_summonees: Список рассылок для призыва
            is_add_to_followers: Добавить автора в наблюдатели
            notify: Уведомлять пользователей
            notify_author: Уведомлять автора изменений
            expand: Дополнительная информация (all, html, attachments, reactions)

        Returns:
            Dict[str, Any]: Обновлённый комментарий
        """
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(comment_id, str) or not comment_id.strip():
            raise ValueError("comment_id должен быть непустой строкой")

        if text is None and attachment_ids is None and summonees is None and maillist_summonees is None:
            raise ValueError("Необходимо указать хотя бы один параметр для обновления")

        self.logger.info(f"Обновление комментария {comment_id} сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/comments/{comment_id}'

        params = {}
        if is_add_to_followers is not None:
            params['isAddToFollowers'] = 'true' if is_add_to_followers else 'false'
        if notify is not None:
            params['notify'] = 'true' if notify else 'false'
        if notify_author is not None:
            params['notifyAuthor'] = 'true' if notify_author else 'false'
        if expand is not None:
            params['expand'] = expand

        payload = {}
        if text is not None:
            payload["text"] = text
        if attachment_ids is not None:
            payload["attachmentIds"] = attachment_ids
        if summonees is not None:
            payload["summonees"] = summonees
        if maillist_summonees is not None:
            payload["maillistSummonees"] = maillist_summonees

        result = await self._request(endpoint, 'PATCH', data=payload, params=params or None)

        self.logger.info(f"Комментарий {comment_id} успешно обновлён")
        return result

    async def delete(
        self,
        entity_type: EntityType,
        entity_id: str,
        comment_id: str,
        notify: Optional[bool] = None,
        notify_author: Optional[bool] = None
    ) -> None:
        """
        Удалить комментарий сущности.

        Args:
            entity_type: Тип сущности (project, portfolio, goal)
            entity_id: Идентификатор сущности
            comment_id: Идентификатор комментария
            notify: Уведомлять пользователей
            notify_author: Уведомлять автора изменений
        """
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if not isinstance(comment_id, str) or not comment_id.strip():
            raise ValueError("comment_id должен быть непустой строкой")

        self.logger.info(f"Удаление комментария {comment_id} сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/comments/{comment_id}'

        params = {}
        if notify is not None:
            params['notify'] = 'true' if notify else 'false'
        if notify_author is not None:
            params['notifyAuthor'] = 'true' if notify_author else 'false'

        await self._request(endpoint, 'DELETE', params=params or None)

        self.logger.info(f"Комментарий {comment_id} успешно удалён")
