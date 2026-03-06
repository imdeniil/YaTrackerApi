"""
API модуль для работы с дашбордами в Yandex Tracker
"""

from typing import Dict, Any, Optional, Union, List
from ..base import BaseAPI


class DashboardsAPI(BaseAPI):
    """API для работы с дашбордами"""

    async def create(
        self,
        name: str,
        layout: Optional[str] = None,
        owner: Optional[Union[str, Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Создать дашборд

        Args:
            name: Название дашборда
            layout: Режим отображения виджетов:
                'one-column', 'two-columns', 'three-columns', 'narrow-left-wide-right'
            owner: Владелец (логин или объект с id)

        Returns:
            Dict с параметрами созданного дашборда
        """
        endpoint = "/dashboards/"

        payload: Dict[str, Any] = {"name": name}

        if layout is not None:
            payload["layout"] = layout
        if owner is not None:
            if isinstance(owner, str):
                payload["owner"] = {"id": owner}
            else:
                payload["owner"] = owner

        self.logger.debug(f"Создание дашборда '{name}'")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info(f"Дашборд '{name}' успешно создан")
        return result

    async def create_cycle_time_widget(
        self,
        dashboard_id: Union[str, int],
        description: str,
        query: Optional[str] = None,
        filter: Optional[Dict[str, Any]] = None,
        filter_id: Optional[int] = None,
        from_statuses: Optional[List[Dict[str, str]]] = None,
        to_statuses: Optional[List[Dict[str, str]]] = None,
        excluded_statuses: Optional[List[Dict[str, str]]] = None,
        included_statuses: Optional[List[Dict[str, str]]] = None,
        bucket: Optional[Dict[str, Any]] = None,
        calendar: Optional[int] = None,
        lines: Optional[Dict[str, Any]] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        mode: Optional[str] = None,
        auto_updatable: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Создать виджет «Время цикла»

        Args:
            dashboard_id: Идентификатор дашборда
            description: Название виджета
            query: Фильтр задач на языке запросов
            filter: Фильтр задач по параметрам {"<поле>": "<значение>"}
            filter_id: Идентификатор сохранённого фильтра
            from_statuses: Статусы начала работы [{"key": "open"}]
            to_statuses: Статусы окончания работы [{"key": "closed"}]
            excluded_statuses: Статусы для исключения из расчёта
            included_statuses: Статусы для включения в расчёт
            bucket: Размер шага {"unit": "days"|"weeks"|"months"|"sprints", "count": N}
            calendar: ID календаря рабочего времени
            lines: Настройки линий графика
                {"movingAverage": bool, "standardDeviation": bool,
                 "percentile": [75, 90], "cakePercentile": 83}
            start: Формула начала (например "now()-2w")
            end: Формула окончания (например "now()")
            mode: Режим отображения: 'common-lines' или 'common-lines-and-points'
            auto_updatable: Автообновление графика

        Returns:
            Dict с параметрами созданного виджета
        """
        endpoint = f"/dashboards/{dashboard_id}/widgets/cycleTime"

        payload: Dict[str, Any] = {"description": description}

        if query is not None:
            payload["query"] = query
        if filter is not None:
            payload["filter"] = filter
        if filter_id is not None:
            payload["filterId"] = filter_id
        if from_statuses is not None:
            payload["fromStatuses"] = from_statuses
        if to_statuses is not None:
            payload["toStatuses"] = to_statuses
        if excluded_statuses is not None:
            payload["excludedStatuses"] = excluded_statuses
        if included_statuses is not None:
            payload["includedStatuses"] = included_statuses
        if bucket is not None:
            payload["bucket"] = bucket
        if calendar is not None:
            payload["calendar"] = calendar
        if lines is not None:
            payload["lines"] = lines
        if start is not None:
            payload["start"] = start
        if end is not None:
            payload["end"] = end
        if mode is not None:
            payload["mode"] = mode
        if auto_updatable is not None:
            payload["autoUpdatable"] = auto_updatable

        self.logger.debug(f"Создание виджета 'Время цикла' на дашборде {dashboard_id}")
        result = await self._request(endpoint, method='POST', data=payload)
        self.logger.info(f"Виджет 'Время цикла' успешно создан на дашборде {dashboard_id}")
        return result
