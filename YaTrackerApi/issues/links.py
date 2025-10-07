"""
API модуль для работы со связями между задачами в Yandex Tracker
"""

from typing import Dict, Any, Optional, List, Literal
from ..base import BaseAPI

# Типы связей между задачами
RelationshipType = Literal[
    'relates',              # простая связь
    'is dependent by',      # текущая задача является блокером
    'depends on',           # текущая задача зависит от связываемой
    'is subtask for',       # текущая задача является подзадачей связываемой
    'is parent task for',   # текущая задача является родительской
    'duplicates',           # текущая задача дублирует связываемую
    'is duplicated by',     # связываемая задача дублирует текущую
    'is epic of',           # текущая задача является эпиком связываемой
    'has epic'              # связываемая задача является эпиком текущей
]

class LinksAPI(BaseAPI):
    """API для работы со связями между задачами в Yandex Tracker"""

    async def create(
        self,
        issue_id: str,
        relationship: RelationshipType,
        linked_issue: str
    ) -> Dict[str, Any]:
        """
        Создание связи между задачами

        Создает связь между текущей задачей и указанной связываемой задачей
        с определенным типом отношения.

        Args:
            issue_id: Идентификатор или ключ текущей задачи (например, 'JUNE-3', 'TASK-123')
            relationship: Тип связи между задачами. Доступные типы:
                - 'relates' - простая связь
                - 'is dependent by' - текущая задача является блокером
                - 'depends on' - текущая задача зависит от связываемой
                - 'is subtask for' - текущая задача является подзадачей
                - 'is parent task for' - текущая задача является родительской
                - 'duplicates' - текущая задача дублирует связываемую
                - 'is duplicated by' - связываемая задача дублирует текущую
                - 'is epic of' - текущая задача является эпиком (только для эпиков)
                - 'has epic' - связываемая задача является эпиком (только для эпиков)
            linked_issue: Идентификатор или ключ связываемой задачи

        Returns:
            Dict: Информация о созданной связи с подробностями об обеих задачах

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404, 400, 403)
            ValueError: При некорректных параметрах

        Examples:
            # Простая связь между задачами
            link = await client.issues.links.create(
                'TASK-123',
                'relates',
                'TASK-456'
            )

            # Создание зависимости (TASK-123 зависит от TASK-456)
            link = await client.issues.links.create(
                'TASK-123',
                'depends on',
                'TASK-456'
            )

            # Создание подзадачи (TASK-123 является подзадачей TASK-456)
            link = await client.issues.links.create(
                'TASK-123',
                'is subtask for',
                'TASK-456'
            )

            # Создание родительской задачи (TASK-123 является родительской для TASK-456)
            link = await client.issues.links.create(
                'TASK-123',
                'is parent task for',
                'TASK-456'
            )

            # Создание связи дублирования
            link = await client.issues.links.create(
                'TASK-123',
                'duplicates',
                'TASK-456'
            )

            # Создание эпика (только для задач типа "Эпик")
            epic_link = await client.issues.links.create(
                'EPIC-1',
                'is epic of',
                'TASK-123'
            )

            # Результат содержит информацию о связи
            print(f"Создана связь: {link['object']['key']} -> {link['subject']['key']}")
            print(f"Тип связи: {link['relationship']['display']}")
        """

        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        if not linked_issue or not isinstance(linked_issue, str):
            raise ValueError("linked_issue должен быть непустой строкой")

        if not relationship:
            raise ValueError("relationship должен быть указан")

        # Валидируем тип связи
        valid_relationships = {
            'relates', 'is dependent by', 'depends on', 'is subtask for',
            'is parent task for', 'duplicates', 'is duplicated by',
            'is epic of', 'has epic'
        }

        if relationship not in valid_relationships:
            raise ValueError(f"Неподдерживаемый тип связи: {relationship}. "
                           f"Доступные: {', '.join(valid_relationships)}")

        endpoint = f"/issues/{issue_id}/links"

        # Подготавливаем payload
        payload = {
            'relationship': relationship,
            'issue': linked_issue
        }

        self.logger.info(f"Создание связи между задачами: {issue_id} -> {linked_issue}")
        self.logger.debug(f"Тип связи: {relationship}")

        try:
            result = await self._request(endpoint, method='POST', data=payload)

            # Логгируем успешный результат
            object_key = result.get('object', {}).get('key', issue_id)
            subject_key = result.get('subject', {}).get('key', linked_issue)
            relationship_display = result.get('relationship', {}).get('display', relationship)

            self.logger.info(f"Связь успешно создана: {object_key} [{relationship_display}] {subject_key}")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при создании связи между {issue_id} и {linked_issue}: {e}")
            raise

    async def get(self, issue_id: str) -> List[Dict[str, Any]]:
        """
        Получение всех связей задачи

        Возвращает список всех связей указанной задачи, включая информацию
        о связанных задачах и типах отношений.

        Args:
            issue_id: Идентификатор или ключ задачи (например, 'JUNE-2', 'TASK-123')

        Returns:
            List[Dict]: Список связей с подробной информацией о каждой связи

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404, 400, 403)
            ValueError: При некорректных параметрах

        Examples:
            # Получение всех связей задачи
            links = await client.issues.links.get('TASK-123')

            # Анализ связей
            for link in links:
                object_key = link['object']['key']
                subject_key = link['subject']['key']
                relationship = link['relationship']['display']
                print(f"Связь: {object_key} [{relationship}] {subject_key}")

            # Фильтрация связей по типу
            dependencies = [
                link for link in links
                if link['relationship']['key'] == 'depends on'
            ]

            subtasks = [
                link for link in links
                if link['relationship']['key'] == 'is parent task for'
            ]

            # Получение связанных задач определенного типа
            blocked_tasks = [
                link['subject']['key'] for link in links
                if link['relationship']['key'] == 'is dependent by'
            ]

            # Результат содержит полную информацию о связях
            if links:
                print(f"Найдено {len(links)} связей для задачи {issue_id}")
                for link in links:
                    print(f"  - {link['object']['key']} -> {link['subject']['key']}")
                    print(f"    Тип: {link['relationship']['display']}")
        """

        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        endpoint = f"/issues/{issue_id}/links"

        self.logger.info(f"Получение связей для задачи: {issue_id}")

        try:
            result = await self._request(endpoint, method='GET')

            # Логгируем результат
            links_count = len(result) if isinstance(result, list) else 0
            self.logger.info(f"Получено {links_count} связей для задачи {issue_id}")

            if links_count > 0:
                # Группируем связи по типам для логирования
                relationship_counts = {}
                for link in result:
                    rel_type = link.get('relationship', {}).get('key', 'unknown')
                    relationship_counts[rel_type] = relationship_counts.get(rel_type, 0) + 1

                self.logger.debug(f"Распределение связей по типам: {relationship_counts}")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при получении связей для задачи {issue_id}: {e}")
            raise

    async def delete(self, issue_id: str, link_id: str) -> Dict[str, Any]:
        """
        Удаление связи между задачами

        Удаляет указанную связь между задачами по идентификатору связи.
        После удаления связь полностью исчезает из обеих связанных задач.

        Args:
            issue_id: Идентификатор или ключ задачи (например, 'JUNE-2', 'TASK-123')
            link_id: Идентификатор связи для удаления (получается из метода get())

        Returns:
            Dict: Информация об удаленной связи

        Raises:
            aiohttp.ClientResponseError: При ошибках HTTP запроса (404, 400, 403)
            ValueError: При некорректных параметрах

        Examples:
            # Получение связей и удаление конкретной связи
            links = await client.issues.links.get('TASK-123')
            if links:
                link_to_delete = links[0]
                link_id = link_to_delete['id']

                result = await client.issues.links.delete('TASK-123', link_id)
                print(f"Удалена связь: {result['object']['key']} -> {result['subject']['key']}")

            # Удаление всех связей определенного типа
            links = await client.issues.links.get('TASK-123')
            dependency_links = [
                link for link in links
                if link['relationship']['key'] == 'depends on'
            ]

            for link in dependency_links:
                await client.issues.links.delete('TASK-123', link['id'])
                print(f"Удалена зависимость: {link['subject']['key']}")

            # Удаление связи дублирования
            links = await client.issues.links.get('DUPLICATE-TASK')
            duplicate_links = [
                link for link in links
                if link['relationship']['key'] == 'duplicates'
            ]

            if duplicate_links:
                result = await client.issues.links.delete(
                    'DUPLICATE-TASK',
                    duplicate_links[0]['id']
                )
                print("Связь дублирования удалена")

            # Пакетное удаление всех связей задачи
            links = await client.issues.links.get('TASK-123')
            deleted_count = 0

            for link in links:
                try:
                    await client.issues.links.delete('TASK-123', link['id'])
                    deleted_count += 1
                except Exception as e:
                    print(f"Не удалось удалить связь {link['id']}: {e}")

            print(f"Удалено {deleted_count} из {len(links)} связей")

            # Результат содержит информацию об удаленной связи
            print(f"Удаленная связь: {result['relationship']['display']}")
        """

        if not issue_id or not isinstance(issue_id, str):
            raise ValueError("issue_id должен быть непустой строкой")

        if not link_id or not isinstance(link_id, str):
            raise ValueError("link_id должен быть непустой строкой")

        endpoint = f"/issues/{issue_id}/links/{link_id}"

        self.logger.info(f"Удаление связи {link_id} для задачи: {issue_id}")

        try:
            result = await self._request(endpoint, method='DELETE')

            # Логгируем успешное удаление
            if result:
                object_key = result.get('object', {}).get('key', issue_id)
                subject_key = result.get('subject', {}).get('key', 'N/A')
                relationship_display = result.get('relationship', {}).get('display', 'N/A')

                self.logger.info(f"Связь успешно удалена: {object_key} [{relationship_display}] {subject_key}")
            else:
                self.logger.info(f"Связь {link_id} успешно удалена для задачи {issue_id}")

            return result if result else {"status": "deleted", "link_id": link_id}

        except Exception as e:
            self.logger.error(f"Ошибка при удалении связи {link_id} для задачи {issue_id}: {e}")
            raise