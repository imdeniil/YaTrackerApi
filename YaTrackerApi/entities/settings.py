from typing import Dict, Any, List, Optional
from ..base import BaseAPI

EntityType = str


class EntitySettingsAPI(BaseAPI):
    """API для работы с настройками доступа сущностей (проекты, портфели, цели) в Yandex Tracker"""

    async def get(
        self,
        entity_type: EntityType,
        entity_id: str
    ) -> Dict[str, Any]:
        """
        Получить настройки доступа сущности.

        Args:
            entity_type: Тип сущности (project, portfolio, goal)
            entity_id: Идентификатор сущности

        Returns:
            Dict[str, Any]: Настройки доступа (acl, permissionSources, parentEntities)
        """
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        self.logger.info(f"Получение настроек доступа сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/extendedPermissions'
        result = await self._request(endpoint, 'GET')

        self.logger.info(f"Настройки доступа сущности {entity_type} '{entity_id}' получены")
        return result

    async def update(
        self,
        entity_type: EntityType,
        entity_id: str,
        permission_sources: Optional[Any] = None,
        acl: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Изменить настройки доступа сущности.

        Args:
            entity_type: Тип сущности (project, portfolio, goal)
            entity_id: Идентификатор сущности
            permission_sources: Источники наследования прав (ID родительской сущности или [] для отключения)
            acl: Настройки прав доступа. Формат:
                {
                    "grant": {
                        "READ": {"users": [...], "groups": [...], "roles": [...]},
                        "WRITE": {"users": [...], "groups": [...], "roles": [...]},
                        "GRANT": {"users": [...], "groups": [...], "roles": [...]}
                    },
                    "revoke": {
                        "READ": {"users": [...], "groups": [...], "roles": [...]},
                        ...
                    }
                }
                Роли: AUTHOR, OWNER, CLIENT, FOLLOWER, MEMBER

        Returns:
            Dict[str, Any]: Обновлённые настройки доступа
        """
        if not isinstance(entity_type, str) or entity_type not in ["project", "portfolio", "goal"]:
            raise ValueError("entity_type должен быть одним из: project, portfolio, goal")

        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id должен быть непустой строкой")

        if permission_sources is None and acl is None:
            raise ValueError("Необходимо указать хотя бы один параметр: permission_sources или acl")

        self.logger.info(f"Обновление настроек доступа сущности {entity_type}: {entity_id}")

        endpoint = f'/entities/{entity_type}/{entity_id}/extendedPermissions'

        payload = {}
        if permission_sources is not None:
            payload["permissionSources"] = permission_sources
        if acl is not None:
            payload["acl"] = acl

        result = await self._request(endpoint, 'PATCH', data=payload)

        self.logger.info(f"Настройки доступа сущности {entity_type} '{entity_id}' обновлены")
        return result
