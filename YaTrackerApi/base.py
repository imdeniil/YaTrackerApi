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
                    response.raise_for_status()
                
                self.logger.info(f"Запрос к {endpoint} выполнен успешно")
                
                # Пытаемся распарсить JSON
                try:
                    result = json.loads(response_text)
                    self.logger.debug(f"Ответ успешно распарсен как JSON")
                    return result
                except json.JSONDecodeError:
                    self.logger.warning(f"Ответ не является валидным JSON: {response_text}")
                    return {"raw_response": response_text}
                
        except aiohttp.ClientConnectionError as e:
            self.logger.error(f"Ошибка соединения: {e}")
            raise
        except aiohttp.ClientResponseError as e:
            self.logger.error(f"HTTP ошибка {e.status}: {e.message}")
            if response:
                try:
                    error_text = await response.text()
                    self.logger.error(f"Текст ошибки: {error_text}")
                except:
                    self.logger.error("Не удалось прочитать текст ошибки")
            raise
        except asyncio.TimeoutError as e:
            self.logger.error(f"Ошибка тайм-аута: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Ошибка запроса: {type(e).__name__}: {e}")
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
