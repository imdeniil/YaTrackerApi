"""
API модуль для работы с внешними интеграциями в Yandex Tracker
"""

from ..base import BaseAPI


class ExternalAPI(BaseAPI):
    """Точка входа для внешних интеграций"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._links = None

    @property
    def links(self):
        """Доступ к API для работы с внешними связями"""
        if self._links is None:
            from .links import ExternalLinksAPI
            self._links = ExternalLinksAPI(self.client)
        return self._links
