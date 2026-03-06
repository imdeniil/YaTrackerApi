"""
API модуль для работы с автоматизациями в Yandex Tracker
"""

from ..base import BaseAPI


class AutomationsAPI(BaseAPI):
    """API для работы с автоматизациями (автодействия, триггеры, макросы)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._autoactions = None
        self._triggers = None
        self._macros = None

    @property
    def autoactions(self):
        """Доступ к API для работы с автодействиями"""
        if self._autoactions is None:
            from .autoactions import AutoactionsAPI
            self._autoactions = AutoactionsAPI(self.client)
        return self._autoactions

    @property
    def triggers(self):
        """Доступ к API для работы с триггерами"""
        if self._triggers is None:
            from .triggers import TriggersAPI
            self._triggers = TriggersAPI(self.client)
        return self._triggers

    @property
    def macros(self):
        """Доступ к API для работы с макросами"""
        if self._macros is None:
            from .macros import MacrosAPI
            self._macros = MacrosAPI(self.client)
        return self._macros
