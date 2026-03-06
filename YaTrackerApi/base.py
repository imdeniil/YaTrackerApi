"""
Базовые классы для Yandex Tracker API Client
"""

import asyncio
import aiohttp
import json
import logging
import ssl
from typing import Dict, Any, Optional, Union, List
from abc import ABC
from .exceptions import raise_for_status, TrackerAPIError

class BaseAPI(ABC):
    """Базовый класс для всех API модулей"""
    
    def __init__(self, client: 'YandexTrackerClient'):
        """
        Инициализация API модуля
        
        Args:
            client: Экземпляр основного клиента YandexTrackerClient
        """
        self.client = client
        self.logger = client.logger
    
    async def _request(self, endpoint: str, method: str = 'GET', 
                      data: Optional[Dict] = None, 
                      params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Выполнение HTTP запроса через основной клиент
        
        Args:
            endpoint: Конечная точка API (например, '/issues/TASK-123')
            method: HTTP метод (GET, POST, PUT, PATCH, DELETE)
            data: Данные для отправки в теле запроса (JSON)
            params: Параметры запроса (query string)
            
        Returns:
            Dict с ответом от API
            
        Raises:
            aiohttp.ClientError: При ошибках HTTP запроса
        """
        return await self.client.request(endpoint, method, data, params)


class YandexTrackerClient:
    """Основной клиент для работы с Yandex Tracker API"""

    def __init__(self, oauth_token: str, org_id: str, log_level: str = "INFO"):
        """
        Инициализация клиента
        
        Args:
            oauth_token: OAuth токен для авторизации
            org_id: ID организации в Yandex Cloud  
            log_level: Уровень логгирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.base_url = 'https://api.tracker.yandex.net/v3'
        self.oauth_token = oauth_token
        self.org_id = org_id
        self.headers = {
            'Authorization': f'OAuth {oauth_token}',
            'X-Org-ID': org_id,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self._session = None
        
        # Настройка логгирования
        self.logger = logging.getLogger(f"{__name__}.YandexTrackerClient")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Создаем handler только если его еще нет
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        # Инициализация API модулей (lazy loading)
        self._issues = None
        self._entities = None
        self._users = None
        self._queues = None
        self._filters = None
        self._automations = None
        self._boards = None
        self._dashboards = None
        self._components = None
        self._worklog = None
        self._imports = None
        self._external = None
    
    @property
    def issues(self):
        """Доступ к API модулю для работы с задачами"""
        if self._issues is None:
            from .issues import IssuesAPI
            self._issues = IssuesAPI(self)
        return self._issues

    @property
    def entities(self):
        """Доступ к API модулю для работы с сущностями (проекты, портфели, цели)"""
        if self._entities is None:
            from .entities import EntitiesAPI
            self._entities = EntitiesAPI(self)
        return self._entities

    @property
    def users(self):
        """Доступ к API модулю для работы с пользователями"""
        if self._users is None:
            from .users import UsersAPI
            self._users = UsersAPI(self)
        return self._users

    @property
    def queues(self):
        """Доступ к API модулю для работы с очередями"""
        if self._queues is None:
            from .queues import QueuesAPI
            self._queues = QueuesAPI(self)
        return self._queues

    @property
    def automations(self):
        """Доступ к API модулю для работы с автоматизациями"""
        if self._automations is None:
            from .automations import AutomationsAPI
            self._automations = AutomationsAPI(self)
        return self._automations

    @property
    def external(self):
        """Доступ к API модулю для работы с внешними интеграциями"""
        if self._external is None:
            from .external import ExternalAPI
            self._external = ExternalAPI(self)
        return self._external

    @property
    def imports(self):
        """Доступ к API модулю для импорта данных"""
        if self._imports is None:
            from .imports import ImportsAPI
            self._imports = ImportsAPI(self)
        return self._imports

    @property
    def worklog(self):
        """Доступ к API модулю для работы с учётом времени"""
        if self._worklog is None:
            from .worklog import WorklogAPI
            self._worklog = WorklogAPI(self)
        return self._worklog

    @property
    def components(self):
        """Доступ к API модулю для работы с компонентами"""
        if self._components is None:
            from .components import ComponentsAPI
            self._components = ComponentsAPI(self)
        return self._components

    @property
    def dashboards(self):
        """Доступ к API модулю для работы с дашбордами"""
        if self._dashboards is None:
            from .dashboards import DashboardsAPI
            self._dashboards = DashboardsAPI(self)
        return self._dashboards

    @property
    def boards(self):
        """Доступ к API модулю для работы с досками задач"""
        if self._boards is None:
            from .boards import BoardsAPI
            self._boards = BoardsAPI(self)
        return self._boards

    @property
    def filters(self):
        """Доступ к API модулю для работы с фильтрами"""
        if self._filters is None:
            from .filters import FiltersAPI
            self._filters = FiltersAPI(self)
        return self._filters

    async def __aenter__(self):
        """Async context manager entry"""
        self.logger.debug("Инициализация HTTP сессии")
        
        # Создаем SSL контекст
        ssl_context = ssl.create_default_context()
        
        # Настройки подключения
        connector = aiohttp.TCPConnector(
            ssl=ssl_context,
            limit=100,
            limit_per_host=30,
            ttl_dns_cache=300,
            use_dns_cache=True,
        )
        
        # Настройки таймаутов
        timeout = aiohttp.ClientTimeout(
            total=30,      # общий таймаут
            connect=10,    # таймаут подключения
            sock_read=10   # таймаут чтения
        )
        
        self._session = aiohttp.ClientSession(
            headers=self.headers,
            connector=connector,
            timeout=timeout
        )
        
        self.logger.info("HTTP сессия успешно инициализирована")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self._session:
            await self._session.close()
            self.logger.debug("HTTP сессия закрыта")

    @property
    def session(self) -> aiohttp.ClientSession:
        """Получение сессии"""
        if self._session is None:
            raise RuntimeError("Client must be used as async context manager")
        return self._session

    async def request(self, endpoint: str, method: str = 'GET', 
                     data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Базовый метод для выполнения HTTP запросов
        
        Args:
            endpoint: Конечная точка API (например, '/issues/TASK-123')
            method: HTTP метод (GET, POST, PUT, PATCH, DELETE)
            data: Данные для отправки в теле запроса (JSON)
            params: Параметры запроса (query string)
            
        Returns:
            Dict с ответом от API
            
        Raises:
            aiohttp.ClientError: При ошибках HTTP запроса
        """
        url = f"{self.base_url}{endpoint}"
        
        # Логгирование запроса
        self.logger.info(f"Выполнение {method} запроса к: {endpoint}")
        self.logger.debug(f"Полный URL: {url}")
        self.logger.debug(f"Заголовки: {self.headers}")
        if params:
            self.logger.debug(f"Параметры запроса: {params}")
        if data:
            self.logger.debug(f"Данные запроса: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        response = None
        try:
            kwargs = {
                'method': method,
                'url': url,
                'params': params
            }
            
            if data is not None:
                kwargs['json'] = data
                
            async with self.session.request(**kwargs) as response:
                self.logger.debug(f"Статус ответа: {response.status}")
                self.logger.debug(f"Заголовки ответа: {dict(response.headers)}")
                
                # Читаем текст ответа перед проверкой статуса
                response_text = await response.text()
                
                if response.status >= 400:
                    self.logger.error(f"HTTP ошибка {response.status}: {response_text}")
                    raise_for_status(response.status, response_text, url=url, method=method)

                self.logger.info(f"Запрос к {endpoint} выполнен успешно")

                # Пытаемся распарсить JSON
                try:
                    result = json.loads(response_text)
                    self.logger.debug(f"Ответ успешно распарсен как JSON")
                    return result
                except json.JSONDecodeError:
                    self.logger.warning(f"Ответ не является валидным JSON: {response_text}")
                    return {"raw_response": response_text}

        except TrackerAPIError:
            raise
        except aiohttp.ClientConnectionError as e:
            self.logger.error(f"Ошибка соединения: {e}")
            raise
        except asyncio.TimeoutError as e:
            self.logger.error(f"Ошибка тайм-аута: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Ошибка запроса: {type(e).__name__}: {e}")
            raise

    async def request_binary(self, endpoint: str, method: str = 'GET',
                            params: Optional[Dict] = None) -> bytes:
        """
        HTTP запрос с бинарным ответом (для скачивания файлов)
        """
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"Выполнение {method} запроса (binary) к: {endpoint}")

        try:
            async with self.session.request(method=method, url=url, params=params) as response:
                if response.status >= 400:
                    error_text = await response.text()
                    self.logger.error(f"HTTP ошибка {response.status}: {error_text}")
                    raise_for_status(response.status, error_text, url=url, method=method)

                data = await response.read()
                self.logger.info(f"Получено {len(data)} байт из {endpoint}")
                return data

        except TrackerAPIError:
            raise
        except aiohttp.ClientConnectionError as e:
            self.logger.error(f"Ошибка соединения: {e}")
            raise

    async def request_multipart(self, endpoint: str, file_data: bytes,
                                filename: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        HTTP POST запрос с multipart/form-data (для загрузки файлов)
        """
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"Загрузка файла '{filename}' ({len(file_data)} байт) к: {endpoint}")

        form = aiohttp.FormData()
        form.add_field('file', file_data, filename=filename)

        # Создаём отдельный запрос без сессионного Content-Type,
        # чтобы aiohttp сам выставил multipart/form-data с boundary
        headers = {k: v for k, v in self.headers.items() if k.lower() != 'content-type'}

        try:
            connector = aiohttp.TCPConnector(ssl=True)
            async with aiohttp.ClientSession(headers=headers, connector=connector) as upload_session:
                async with upload_session.post(url, data=form, params=params) as response:
                    if response.status >= 400:
                        error_text = await response.text()
                        self.logger.error(f"HTTP ошибка {response.status}: {error_text}")
                        raise_for_status(response.status, error_text, url=url, method='POST')

                    result = await response.json()
                    self.logger.info(f"Файл '{filename}' успешно загружен")
                    return result

        except TrackerAPIError:
            raise
        except aiohttp.ClientConnectionError as e:
            self.logger.error(f"Ошибка соединения: {e}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """
        Проверка работоспособности API соединения
        
        Выполняет запрос к /myself для проверки:
        - Корректности OAuth токена
        - Корректности Organization ID
        - Доступности API Yandex Tracker
        
        Returns:
            Dict с информацией о текущем пользователе
            
        Raises:
            aiohttp.ClientResponseError: При ошибках авторизации или API
            
        Examples:
            # Проверка подключения перед основной работой
            try:
                user_info = await client.health_check()
                print(f"API доступен. Пользователь: {user_info['display']}")
            except aiohttp.ClientResponseError:
                print("Проблемы с подключением к API")
        """
        self.logger.info("Выполнение проверки работоспособности API")
        try:
            result = await self.request('/myself')
            self.logger.info(f"Health check успешен. Пользователь: {result.get('display', 'Неизвестно')}")
            return result
        except Exception as e:
            self.logger.error(f"Health check неудачен: {e}")
            raise
