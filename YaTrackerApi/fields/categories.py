from typing import List, Dict, Any, Optional
from ..base import BaseAPI

# Типы данных для категорий полей
CategoryNameType = Dict[str, str]  # {"en": "English name", "ru": "Русское название"}


class FieldCategoriesAPI(BaseAPI):
    """API для работы с категориями полей задач"""

    async def list(self) -> List[Dict[str, Any]]:
        """
        Получение списка категорий полей задач.

        Возвращает все категории с их ID, названиями и ссылками.

        Returns:
            List[Dict[str, Any]]: Список категорий. Каждая категория содержит:
                - id (str): Уникальный идентификатор категории
                - name (str): Название категории
                - self (str): URL категории в API
                - version (int): Версия категории (для оптимистичной блокировки)

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Example:
            categories = await client.issues.fields.categories.list()
            for cat in categories:
                print(f"{cat['name']}: {cat['id']}")
        """
        self.logger.info("Получение списка категорий полей")

        endpoint = '/fields/categories'
        result = await self._request(endpoint, 'GET')

        self.logger.info(f"Получено {len(result)} категорий")

        return result

    async def create(
        self,
        name: CategoryNameType,
        order: int,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Создание новой категории полей задач.

        Args:
            name (CategoryNameType): Название категории на разных языках
                                {"en": "English name", "ru": "Русское название"}
            order (int): Вес поля при отображении в интерфейсе.
                        Поля с меньшим весом отображаются выше полей с большим весом.
            description (Optional[str]): Описание категории

        Returns:
            Dict[str, Any]: Информация о созданной категории

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса

        Example:
            category = await client.issues.fields.categories.create(
                name={
                    "en": "Project Management",
                    "ru": "Управление проектами"
                },
                order=400,
                description="Поля для управления проектами и задачами"
            )
        """
        if not isinstance(name, dict) or not name.get('en') or not name.get('ru'):
            raise ValueError("name должен содержать ключи 'en' и 'ru' с непустыми значениями")

        if not isinstance(order, int):
            raise ValueError("order должен быть числом")

        self.logger.info(f"Создание категории полей '{name['ru']}' (порядок: {order})")

        payload = {
            "name": name,
            "order": order
        }

        if description is not None:
            payload["description"] = str(description)

        self.logger.debug(f"Параметры создания категории: {payload}")

        endpoint = '/fields/categories'
        result = await self._request(endpoint, 'POST', data=payload)

        self.logger.info(f"Категория '{name['ru']}' успешно создана с ID: {result.get('id')}")

        return result

    async def update(
        self,
        category_id: str,
        version: str,
        name: Optional[CategoryNameType] = None,
        order: Optional[int] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Изменение категории полей задач.

        Args:
            category_id: ID категории для обновления
            version: Текущая версия категории (для оптимистичной блокировки)
            name: Новое название категории на разных языках
                  {"en": "English name", "ru": "Русское название"}
            order: Новый вес поля при отображении в интерфейсе
            description: Новое описание категории

        Returns:
            Dict: Информация об обновлённой категории

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
        """
        if not isinstance(category_id, str) or not category_id.strip():
            raise ValueError("category_id должен быть непустой строкой")

        if not isinstance(version, str) or not version.strip():
            raise ValueError("version должен быть непустой строкой")

        update_params = [name, order, description]
        if all(param is None for param in update_params):
            raise ValueError("Необходимо указать хотя бы один параметр для обновления")

        if name is not None:
            if not isinstance(name, dict) or not name.get('en') or not name.get('ru'):
                raise ValueError("name должен содержать ключи 'en' и 'ru' с непустыми значениями")

        payload: Dict[str, Any] = {}
        if name is not None:
            payload['name'] = name
        if order is not None:
            payload['order'] = order
        if description is not None:
            payload['description'] = str(description)

        endpoint = f'/fields/categories/{category_id}'
        params = {'version': version}
        result = await self._request(endpoint, 'PATCH', data=payload, params=params)

        self.logger.info(f"Категория '{category_id}' успешно обновлена")
        return result
