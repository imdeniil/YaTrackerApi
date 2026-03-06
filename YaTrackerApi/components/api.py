"""
API модуль для работы с компонентами в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class ComponentsAPI(BaseAPI):
    """API для работы с компонентами"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._permissions = None

    @property
    def permissions(self):
        """Доступ к API для работы с правами доступа к компонентам"""
        if self._permissions is None:
            from .permissions import ComponentPermissionsAPI
            self._permissions = ComponentPermissionsAPI(self.client)
        return self._permissions

    async def list(self) -> List[Dict[str, Any]]:
        """
        Получить список всех компонентов

        Returns:
            List с компонентами
        """
        endpoint = "/components"

        self.logger.debug("Получение списка компонентов")
        result = await self._request(endpoint, method='GET')
        self.logger.info("Список компонентов успешно получен")
        return result

    async def create(
        self,
        name: str,
        queue: str,
        description: Optional[str] = None,
        lead: Optional[str] = None,
        assign_auto: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Создать компонент

        Args:
            name: Название компонента
            queue: Ключ очереди
            description: Описание компонента
            lead: Логин владельца компонента
            assign_auto: Автоматически назначать владельца исполнителем

        Returns:
            Dict с параметрами созданного компонента
        """
        endpoint = "/components"

        payload: Dict[str, Any] = {
            "name": name,
            "queue": queue
        }

        if description is not None:
            payload["description"] = description
        if lead is not None:
            payload["lead"] = lead
        if assign_auto is not None:
            payload["assignAuto"] = assign_auto

        self.logger.debug(f"Создание компонента '{name}' в очереди {queue}")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info(f"Компонент '{name}' успешно создан")
        return result

    async def update(
        self,
        component_id: Union[str, int],
        version: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        lead: Optional[str] = None,
        assign_auto: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Редактировать компонент

        Если version не указан, автоматически получает текущую версию.

        Args:
            component_id: Идентификатор компонента
            version: Версия компонента для оптимистичной блокировки
            name: Новое название компонента
            description: Новое описание
            lead: Новый логин владельца
            assign_auto: Автоматически назначать владельца исполнителем

        Returns:
            Dict с обновленными параметрами компонента
        """
        endpoint = f"/components/{component_id}"

        if version is None:
            # get_all() может не содержать свежесозданные компоненты,
            # поэтому запрашиваем конкретный компонент для получения версии
            # Отдельного GET /components/{id} нет — ищем в get_all или пробуем PATCH
            components = await self.list()
            for c in components:
                if str(c.get('id')) == str(component_id):
                    version = c.get('version')
                    break

        params = {"version": version} if version is not None else None

        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if lead is not None:
            payload["lead"] = lead
        if assign_auto is not None:
            payload["assignAuto"] = assign_auto

        self.logger.debug(f"Обновление компонента {component_id}")
        result = await self._request(endpoint, method='PATCH', data=payload, params=params)
        self.logger.info(f"Компонент {component_id} успешно обновлен")
        return result

