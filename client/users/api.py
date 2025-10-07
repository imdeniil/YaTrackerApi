from typing import List, Dict, Any, Union, Optional, overload
from ..base import BaseAPI

class UsersAPI(BaseAPI):
    """API для работы с пользователями в Yandex Tracker"""

    @overload
    async def get(self) -> List[Dict[str, Any]]: ...

    @overload
    async def get(self, user_id: Union[str, int]) -> Dict[str, Any]: ...

    async def get(self, user_id: Optional[Union[str, int]] = None) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Получение информации о пользователях.

        Args:
            user_id: Опционально. Логин или ID пользователя.
                     Если не указан - возвращает список всех пользователей организации.

        Returns:
            - Если user_id указан: Dict с информацией о пользователе
            - Если user_id None: List всех пользователей организации

        Raises:
            ValueError: При некорректных параметрах (только для конкретного пользователя)
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если пользователь не найден (только для конкретного пользователя)
                - 403 если недостаточно прав доступа

        Examples:
            # Получение всех пользователей организации
            users = await client.users.get()

            # Анализ полученных пользователей
            for user in users:
                user_id = user.get('id')
                login = user.get('login')
                display_name = user.get('display')
                print(f"{display_name} ({login})")

            # Фильтрация активных пользователей
            active_users = [
                user for user in users
                if not user.get('dismissed', False)
            ]
            print(f"Активных пользователей: {len(active_users)}")

            # Получение конкретного пользователя по логину
            user = await client.users.get('username')
            print(f"Имя: {user['display']}")
            print(f"Email: {user['email']}")

            # Получение пользователя по ID
            user = await client.users.get(123456)

            # Проверка статуса пользователя
            if user.get('dismissed', False):
                print("Статус: Уволен")
            else:
                print("Статус: Активен")

            # Информация о департаменте
            if 'department' in user:
                dept_name = user['department'].get('display', 'Не указан')
                print(f"Департамент: {dept_name}")

            # Информация о руководителе
            if 'chief' in user:
                chief_name = user['chief'].get('display', 'Не указан')
                print(f"Руководитель: {chief_name}")
        """

        # Если user_id не указан - возвращаем список всех пользователей
        if user_id is None:
            self.logger.info("Получение списка пользователей организации")

            endpoint = '/users'
            result = await self._request(endpoint, 'GET')

            # Проверяем, что получили список
            if not isinstance(result, list):
                self.logger.warning(f"Неожиданный тип ответа: {type(result)}")
                result = []

            users_count = len(result)
            self.logger.info(f"Получено {users_count} пользователей")

            if users_count > 0:
                # Анализируем пользователей для логирования
                active_users = [user for user in result if not user.get('dismissed', False)]
                dismissed_users = [user for user in result if user.get('dismissed', False)]

                active_count = len(active_users)
                dismissed_count = len(dismissed_users)

                self.logger.debug(f"Активных пользователей: {active_count}")
                self.logger.debug(f"Уволенных пользователей: {dismissed_count}")

                # Анализируем департаменты
                departments = set()
                for user in result:
                    if 'department' in user and 'display' in user['department']:
                        departments.add(user['department']['display'])

                if departments:
                    self.logger.debug(f"Количество департаментов: {len(departments)}")

                # Анализируем email домены
                email_domains = set()
                for user in result:
                    if 'email' in user:
                        email = user['email']
                        if '@' in email:
                            domain = email.split('@')[-1]
                            email_domains.add(domain)

                if email_domains:
                    self.logger.debug(f"Email домены: {', '.join(sorted(email_domains))}")

            return result

        # Если user_id указан - получаем конкретного пользователя
        else:
            # Валидация параметров
            if not isinstance(user_id, (str, int)):
                raise ValueError("user_id должен быть строкой или числом")

            if isinstance(user_id, str) and not user_id.strip():
                raise ValueError("user_id (строка) должен быть непустым")

            # Преобразуем в строку для URL
            user_identifier = str(user_id).strip()

            self.logger.info(f"Получение информации о пользователе: {user_identifier}")

            endpoint = f'/users/{user_identifier}'
            result = await self._request(endpoint, 'GET')

            # Логируем полученную информацию
            if isinstance(result, dict):
                login = result.get('login', 'N/A')
                display_name = result.get('display', 'N/A')
                user_id_response = result.get('id', 'N/A')

                self.logger.info(f"Получена информация о пользователе: {display_name} ({login}, ID: {user_id_response})")

                # Дополнительная информация для логирования
                if result.get('dismissed', False):
                    self.logger.debug(f"Пользователь {login} уволен")
                    if 'dismissalDate' in result:
                        dismiss_date = result['dismissalDate']
                        self.logger.debug(f"Дата увольнения: {dismiss_date}")
                else:
                    self.logger.debug(f"Пользователь {login} активен")

                if 'department' in result:
                    dept_name = result['department'].get('display', 'N/A')
                    self.logger.debug(f"Департамент: {dept_name}")

                if 'chief' in result:
                    chief_name = result['chief'].get('display', 'N/A')
                    self.logger.debug(f"Руководитель: {chief_name}")

                if result.get('robot', False):
                    self.logger.debug("Это робот/служебный аккаунт")

            return result