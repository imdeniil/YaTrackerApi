from typing import Dict, Any, List, Optional, Union
from ..base import BaseAPI

# Типы данных для комментариев
SummoneesType = Union[str, int, Dict[str, Union[str, int]]]  # Пользователь для призыва

class CommentsAPI(BaseAPI):
    """API для работы с комментариями задач в Yandex Tracker"""

    async def get(
        self,
        issue_id: str,
        expand: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Получение списка комментариев к задаче.

        Args:
            issue_id (str): Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')
            expand (Optional[str]): Дополнительные поля для включения в ответ
                                   - "attachments": вложения
                                   - "html": HTML-разметка комментария
                                   - "all": все дополнительные поля

        Returns:
            List[Dict[str, Any]]: Список комментариев к задаче

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если задача не найдена

        Examples:
            # Получение всех комментариев задачи
            comments = await client.issues.comments.get(issue_id="TASK-123")

            for comment in comments:
                print(f"Комментарий от {comment['createdBy']['display']}")
                print(f"Дата: {comment['createdAt']}")
                print(f"Текст: {comment['text']}")
                print("---")

            # Получение комментариев с вложениями
            comments = await client.issues.comments.get(
                issue_id="TASK-123",
                expand="attachments"
            )

            for comment in comments:
                if comment.get('attachments'):
                    print(f"Комментарий с вложениями: {len(comment['attachments'])}")
                    for attachment in comment['attachments']:
                        print(f"- {attachment['name']} ({attachment['size']} bytes)")

            # Получение комментариев с HTML разметкой
            comments = await client.issues.comments.get(
                issue_id="TASK-123",
                expand="html"
            )

            for comment in comments:
                if comment.get('html'):
                    print(f"HTML версия: {comment['html']}")

            # Получение комментариев со всеми дополнительными полями
            comments = await client.issues.comments.get(
                issue_id="TASK-123",
                expand="all"
            )

            for comment in comments:
                print(f"ID: {comment['id']}")
                print(f"Автор: {comment['createdBy']['display']}")
                print(f"Дата создания: {comment['createdAt']}")
                print(f"Дата изменения: {comment.get('updatedAt', 'N/A')}")
                print(f"Текст: {comment['text']}")

                if comment.get('html'):
                    print(f"HTML: {comment['html']}")

                if comment.get('attachments'):
                    print(f"Вложения: {len(comment['attachments'])}")

                if comment.get('summonees'):
                    summonees = [s.get('display', s) for s in comment['summonees']]
                    print(f"Призванные: {', '.join(summonees)}")

                print("=" * 50)

            # Анализ активности по комментариям
            comments = await client.issues.comments.get(
                issue_id="PROJ-456",
                expand="all"
            )

            # Группировка по авторам
            authors = {}
            for comment in comments:
                author = comment['createdBy']['display']
                if author not in authors:
                    authors[author] = 0
                authors[author] += 1

            print("Активность по комментариям:")
            for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True):
                print(f"- {author}: {count} комментариев")

            # Поиск комментариев с ключевыми словами
            comments = await client.issues.comments.get(issue_id="TASK-789")

            keywords = ["баг", "ошибка", "проблема", "исправить"]
            issues_found = []

            for comment in comments:
                text_lower = comment['text'].lower()
                if any(keyword in text_lower for keyword in keywords):
                    issues_found.append({
                        'author': comment['createdBy']['display'],
                        'date': comment['createdAt'],
                        'text': comment['text'][:100] + "..." if len(comment['text']) > 100 else comment['text']
                    })

            if issues_found:
                print(f"Найдено {len(issues_found)} комментариев с упоминанием проблем:")
                for issue in issues_found:
                    print(f"- {issue['author']} ({issue['date']}): {issue['text']}")
        """
        # Валидация обязательных параметров
        if not isinstance(issue_id, str) or not issue_id.strip():
            raise ValueError("issue_id должен быть непустой строкой")

        # Валидация опциональных параметров
        if expand is not None:
            if not isinstance(expand, str):
                raise ValueError("expand должен быть строкой")
            valid_expand_values = ["attachments", "html", "all"]
            if expand not in valid_expand_values:
                raise ValueError(f"expand должен быть одним из: {', '.join(valid_expand_values)}")

        self.logger.info(f"Получение комментариев задачи: {issue_id}")

        endpoint = f'/issues/{issue_id}/comments'

        # Формирование параметров запроса
        params = {}
        if expand is not None:
            params['expand'] = expand

        self.logger.debug(f"Параметры получения комментариев - Params: {params if params else 'Без параметров'}")

        if expand:
            self.logger.debug(f"Расширенные поля: {expand}")

        result = await self._request(endpoint, 'GET', params=params if params else None)

        # Логируем успешное получение
        comments_count = len(result) if isinstance(result, list) else 0
        self.logger.info(f"Получено {comments_count} комментариев для задачи {issue_id}")

        if comments_count > 0:
            # Анализ полученных комментариев для логирования
            authors = set()
            has_attachments = 0

            for comment in result:
                if isinstance(comment, dict):
                    author = comment.get('createdBy', {})
                    if isinstance(author, dict) and 'display' in author:
                        authors.add(author['display'])

                    if comment.get('attachments'):
                        has_attachments += 1

            self.logger.debug(f"Авторов комментариев: {len(authors)}")
            if has_attachments > 0:
                self.logger.debug(f"Комментариев с вложениями: {has_attachments}")

        return result

    async def update(
        self,
        issue_id: str,
        comment_id: str,
        text: str,
        attachment_ids: Optional[List[str]] = None,
        summonees: Optional[List[SummoneesType]] = None,
        markup_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Обновление существующего комментария к задаче.

        Args:
            issue_id (str): Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')
            comment_id (str): Идентификатор комментария для обновления
            text (str): Новый текст комментария (обязательный параметр)
            attachment_ids (Optional[List[str]]): Идентификаторы временных файлов
                                                для добавления как вложения
            summonees (Optional[List[SummoneesType]]): Призванные пользователи
                                                     - Строка: логин пользователя
                                                     - Число: ID пользователя
                                                     - Объект: {"login": "username"} или {"id": "123"}
            markup_type (Optional[str]): Тип разметки в тексте
                                       - "md" для YFM (Yandex Flavored Markdown)

        Returns:
            Dict[str, Any]: Информация об обновленном комментарии

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если задача или комментарий не найдены
                - 403 если недостаточно прав для редактирования

        Examples:
            # Простое обновление текста комментария
            comment = await client.issues.comments.update(
                issue_id="TASK-123",
                comment_id="12345",
                text="Исправленный текст комментария"
            )

            # Обновление с добавлением призванных пользователей
            comment = await client.issues.comments.update(
                issue_id="TASK-123",
                comment_id="12345",
                text="@username, пожалуйста, проверьте обновленную информацию",
                summonees=["username", "reviewer"]
            )

            # Обновление с Markdown разметкой
            comment = await client.issues.comments.update(
                issue_id="TASK-123",
                comment_id="12345",
                text='''# Обновленные результаты тестирования

**Исправленные функции:**
- ✅ Авторизация (исправлены баги)
- ✅ Создание задач
- ✅ Уведомления (теперь работают)

## Статус
Все проблемы решены, готово к релизу.
                ''',
                markup_type="md",
                summonees=["developer", "qa-team"]
            )

            # Обновление с новыми вложениями
            comment = await client.issues.comments.update(
                issue_id="TASK-123",
                comment_id="12345",
                text="Прикладываю обновленные файлы с результатами",
                attachment_ids=["new-file-123", "updated-report-456"]
            )

            # Полный пример обновления
            comment = await client.issues.comments.update(
                issue_id="PROJ-456",
                comment_id="67890",
                text='''## Финальный статус разработки

**Завершено:**
- Основная логика ✅
- Unit тесты ✅
- Интеграционные тесты ✅
- Документация ✅

**Готово к продакшену!** 🚀

@team-lead @qa-engineer, финальная проверка завершена.
                ''',
                markup_type="md",
                summonees=[{"login": "team-lead"}, {"id": "qa-123"}],
                attachment_ids=["final-report-789", "test-coverage-999"]
            )

            # Удаление призванных (передача пустого списка)
            comment = await client.issues.comments.update(
                issue_id="TASK-123",
                comment_id="12345",
                text="Обычный комментарий без призывов",
                summonees=[]  # Очистка призванных пользователей
            )

            # Результат содержит информацию об обновленном комментарии
            print(f"Комментарий {comment['id']} успешно обновлен")
            print(f"Последнее обновление: {comment.get('updatedAt', 'N/A')}")
            print(f"Автор изменения: {comment.get('updatedBy', {}).get('display', 'N/A')}")
        """
        # Валидация обязательных параметров
        if not isinstance(issue_id, str) or not issue_id.strip():
            raise ValueError("issue_id должен быть непустой строкой")

        if not isinstance(comment_id, str) or not comment_id.strip():
            raise ValueError("comment_id должен быть непустой строкой")

        if not isinstance(text, str) or not text.strip():
            raise ValueError("text должен быть непустой строкой")

        # Валидация опциональных параметров (аналогично create методу)
        if attachment_ids is not None:
            if not isinstance(attachment_ids, list):
                raise ValueError("attachment_ids должен быть списком")
            for attachment_id in attachment_ids:
                if not isinstance(attachment_id, str) or not attachment_id.strip():
                    raise ValueError("Все элементы attachment_ids должны быть непустыми строками")

        if summonees is not None:
            if not isinstance(summonees, list):
                raise ValueError("summonees должен быть списком")

            for i, summonee in enumerate(summonees):
                if isinstance(summonee, str):
                    if not summonee.strip():
                        raise ValueError(f"summonee {i} (строка) должен быть непустым")
                elif isinstance(summonee, int):
                    # ID как число допустимо
                    pass
                elif isinstance(summonee, dict):
                    if "login" not in summonee and "id" not in summonee:
                        raise ValueError(f"summonee {i} (объект) должен содержать 'login' или 'id'")
                    if "login" in summonee:
                        if not isinstance(summonee["login"], str) or not summonee["login"].strip():
                            raise ValueError(f"summonee {i} 'login' должен быть непустой строкой")
                    if "id" in summonee:
                        if not isinstance(summonee["id"], (str, int)):
                            raise ValueError(f"summonee {i} 'id' должен быть строкой или числом")
                else:
                    raise ValueError(f"summonee {i} должен быть строкой, числом или объектом")

        if markup_type is not None and not isinstance(markup_type, str):
            raise ValueError("markup_type должен быть строкой")

        self.logger.info(f"Обновление комментария {comment_id} для задачи: {issue_id}")

        endpoint = f'/issues/{issue_id}/comments/{comment_id}'

        # Формирование тела запроса
        payload = {
            "text": text
        }

        if attachment_ids is not None:
            payload["attachmentIds"] = attachment_ids

        if summonees is not None:
            payload["summonees"] = summonees

        if markup_type is not None:
            payload["markupType"] = markup_type

        self.logger.debug(f"Параметры обновления комментария - Body: {len(payload)} полей")

        # Логируем дополнительную информацию
        if summonees is not None:
            self.logger.debug(f"Призванных пользователей: {len(summonees)}")

        if attachment_ids:
            self.logger.debug(f"Вложений: {len(attachment_ids)}")

        if markup_type:
            self.logger.debug(f"Тип разметки: {markup_type}")

        result = await self._request(endpoint, 'PATCH', data=payload)

        # Логируем успешное обновление
        updated_date = result.get('updatedAt', 'N/A')
        updated_by = result.get('updatedBy', {}).get('display', 'N/A')

        self.logger.info(f"Комментарий {comment_id} успешно обновлен для задачи {issue_id}")
        self.logger.debug(f"Обновлен: {updated_by}, дата: {updated_date}")

        return result

    async def delete(
        self,
        issue_id: str,
        comment_id: str
    ) -> None:
        """
        Удаление комментария к задаче.

        Args:
            issue_id (str): Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')
            comment_id (str): Идентификатор комментария для удаления

        Returns:
            None: Метод не возвращает данные при успешном удалении

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если задача или комментарий не найдены
                - 403 если недостаточно прав для удаления комментария

        Examples:
            # Простое удаление комментария
            await client.issues.comments.delete(
                issue_id="TASK-123",
                comment_id="12345"
            )
            print("Комментарий успешно удален")

            # Удаление с предварительной проверкой существования
            try:
                # Сначала получаем список комментариев
                comments = await client.issues.comments.get(issue_id="TASK-123")

                # Ищем комментарий для удаления
                comment_to_delete = None
                for comment in comments:
                    if comment['text'].startswith('Устаревшая информация'):
                        comment_to_delete = comment
                        break

                if comment_to_delete:
                    await client.issues.comments.delete(
                        issue_id="TASK-123",
                        comment_id=comment_to_delete['id']
                    )
                    print(f"Удален комментарий от {comment_to_delete['createdBy']['display']}")
                else:
                    print("Комментарий для удаления не найден")

            except Exception as e:
                print(f"Ошибка при удалении комментария: {e}")

            # Массовое удаление комментариев по критериям
            comments = await client.issues.comments.get(
                issue_id="PROJ-456",
                expand="all"
            )

            # Удаляем комментарии старше определенной даты
            from datetime import datetime, timedelta
            cutoff_date = datetime.now() - timedelta(days=30)

            deleted_count = 0
            for comment in comments:
                # Парсим дату создания (предполагаем ISO формат)
                created_at = datetime.fromisoformat(
                    comment['createdAt'].replace('Z', '+00:00')
                )

                if created_at < cutoff_date and 'test' in comment['text'].lower():
                    try:
                        await client.issues.comments.delete(
                            issue_id="PROJ-456",
                            comment_id=comment['id']
                        )
                        deleted_count += 1
                        print(f"Удален тестовый комментарий от {comment['createdBy']['display']}")
                    except Exception as e:
                        print(f"Не удалось удалить комментарий {comment['id']}: {e}")

            print(f"Всего удалено комментариев: {deleted_count}")

            # Удаление с обработкой ошибок прав доступа
            try:
                await client.issues.comments.delete(
                    issue_id="SENSITIVE-TASK",
                    comment_id="sensitive-comment-123"
                )
                print("Комментарий успешно удален")
            except aiohttp.ClientResponseError as e:
                if e.status == 403:
                    print("Недостаточно прав для удаления этого комментария")
                elif e.status == 404:
                    print("Комментарий или задача не найдены")
                else:
                    print(f"Ошибка при удалении: {e}")

            # Интерактивное удаление комментариев
            comments = await client.issues.comments.get(issue_id="TASK-789")

            print("Комментарии в задаче:")
            for i, comment in enumerate(comments):
                print(f"{i+1}. {comment['createdBy']['display']}: {comment['text'][:50]}...")

            # В реальном приложении здесь был бы пользовательский ввод
            comment_index = 2  # Например, выбран 3-й комментарий

            if 0 <= comment_index < len(comments):
                selected_comment = comments[comment_index]
                await client.issues.comments.delete(
                    issue_id="TASK-789",
                    comment_id=selected_comment['id']
                )
                print(f"Удален комментарий: {selected_comment['text'][:30]}...")
            else:
                print("Неверный выбор комментария")

            # Проверка результата удаления
            async def safe_delete_comment(issue_id: str, comment_id: str) -> bool:
                '''Безопасное удаление с возвратом статуса операции'''
                try:
                    await client.issues.comments.delete(issue_id, comment_id)
                    return True
                except Exception as e:
                    print(f"Ошибка удаления комментария {comment_id}: {e}")
                    return False

            # Использование
            success = await safe_delete_comment("TASK-123", "comment-456")
            if success:
                print("Комментарий успешно удален")
            else:
                print("Не удалось удалить комментарий")
        """
        # Валидация обязательных параметров
        if not isinstance(issue_id, str) or not issue_id.strip():
            raise ValueError("issue_id должен быть непустой строкой")

        if not isinstance(comment_id, str) or not comment_id.strip():
            raise ValueError("comment_id должен быть непустой строкой")

        self.logger.info(f"Удаление комментария {comment_id} для задачи: {issue_id}")

        endpoint = f'/issues/{issue_id}/comments/{comment_id}'

        # Выполняем DELETE запрос
        await self._request(endpoint, 'DELETE')

        self.logger.info(f"Комментарий {comment_id} успешно удален из задачи {issue_id}")

    async def create(
        self,
        issue_id: str,
        text: str,
        attachment_ids: Optional[List[str]] = None,
        summonees: Optional[List[SummoneesType]] = None,
        maillist_summonees: Optional[List[str]] = None,
        markup_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Создание комментария к задаче.

        Args:
            issue_id (str): Идентификатор или ключ задачи (например, 'JUNE-3', 'TASK-123')
            text (str): Текст комментария (обязательный параметр)
            attachment_ids (Optional[List[str]]): Идентификаторы временных файлов
                                                для добавления как вложения
            summonees (Optional[List[SummoneesType]]): Призванные пользователи
                                                     - Строка: логин пользователя
                                                     - Число: ID пользователя
                                                     - Объект: {"login": "username"} или {"id": "123"}
            maillist_summonees (Optional[List[str]]): Список рассылок, призванных в комментарии
            markup_type (Optional[str]): Тип разметки в тексте
                                       - "md" для YFM (Yandex Flavored Markdown)

        Returns:
            Dict[str, Any]: Информация о созданном комментарии

        Raises:
            ValueError: При некорректных параметрах
            aiohttp.ClientResponseError: При ошибках HTTP запроса
                - 404 если задача не найдена

        Examples:
            # Простой комментарий
            comment = await client.issues.comments.create(
                issue_id="TASK-123",
                text="Работа выполнена и готова к проверке"
            )

            # Комментарий с призванными пользователями
            comment = await client.issues.comments.create(
                issue_id="TASK-123",
                text="@username, пожалуйста, проверьте результат работы",
                summonees=["username", "reviewer"]
            )

            # Комментарий с Markdown разметкой
            comment = await client.issues.comments.create(
                issue_id="TASK-123",
                text='''# Результаты тестирования

**Проверенные функции:**
- ✅ Авторизация
- ✅ Создание задач
- ❌ Уведомления

## Найденные проблемы
1. Уведомления не приходят на email
2. Неправильная валидация формы

**Следующие шаги:**
- Исправить баги
- Повторить тестирование
                ''',
                markup_type="md",
                summonees=["developer", "tester"]
            )

            # Комментарий с вложениями
            comment = await client.issues.comments.create(
                issue_id="TASK-123",
                text="Прикладываю файлы с результатами",
                attachment_ids=["file123", "file456"]
            )

            # Комментарий с призванными рассылками
            comment = await client.issues.comments.create(
                issue_id="TASK-123",
                text="Требуется обсуждение архитектуры",
                maillist_summonees=["architects@company.com", "developers@company.com"]
            )

            # Комментарий с призванными пользователями по ID
            comment = await client.issues.comments.create(
                issue_id="TASK-123",
                text="Пожалуйста, ознакомьтесь с изменениями",
                summonees=[
                    {"login": "username"},
                    {"id": "123456"},
                    789012  # ID как число
                ]
            )

            # Полный пример со всеми параметрами
            comment = await client.issues.comments.create(
                issue_id="PROJ-456",
                text='''## Статус разработки

**Выполнено:**
- Основная логика ✅
- Unit тесты ✅

**В процессе:**
- Интеграционные тесты 🔄

@team-lead @qa-engineer, готов к ревью!
                ''',
                markup_type="md",
                summonees=["team-lead", {"login": "qa-engineer"}],
                maillist_summonees=["dev-team@company.com"],
                attachment_ids=["test-results-123", "coverage-report-456"]
            )

            # Результат содержит информацию о созданном комментарии
            print(f"Создан комментарий: {comment['id']}")
            print(f"Автор: {comment['createdBy']['display']}")
            print(f"Дата: {comment['createdAt']}")
        """
        # Валидация обязательных параметров
        if not isinstance(issue_id, str) or not issue_id.strip():
            raise ValueError("issue_id должен быть непустой строкой")

        if not isinstance(text, str) or not text.strip():
            raise ValueError("text должен быть непустой строкой")

        # Валидация опциональных параметров
        if attachment_ids is not None:
            if not isinstance(attachment_ids, list):
                raise ValueError("attachment_ids должен быть списком")
            for attachment_id in attachment_ids:
                if not isinstance(attachment_id, str) or not attachment_id.strip():
                    raise ValueError("Все элементы attachment_ids должны быть непустыми строками")

        if summonees is not None:
            if not isinstance(summonees, list):
                raise ValueError("summonees должен быть списком")

            for i, summonee in enumerate(summonees):
                if isinstance(summonee, str):
                    if not summonee.strip():
                        raise ValueError(f"summonee {i} (строка) должен быть непустым")
                elif isinstance(summonee, int):
                    # ID как число допустимо
                    pass
                elif isinstance(summonee, dict):
                    if "login" not in summonee and "id" not in summonee:
                        raise ValueError(f"summonee {i} (объект) должен содержать 'login' или 'id'")
                    if "login" in summonee:
                        if not isinstance(summonee["login"], str) or not summonee["login"].strip():
                            raise ValueError(f"summonee {i} 'login' должен быть непустой строкой")
                    if "id" in summonee:
                        if not isinstance(summonee["id"], (str, int)):
                            raise ValueError(f"summonee {i} 'id' должен быть строкой или числом")
                else:
                    raise ValueError(f"summonee {i} должен быть строкой, числом или объектом")

        if maillist_summonees is not None:
            if not isinstance(maillist_summonees, list):
                raise ValueError("maillist_summonees должен быть списком")
            for maillist in maillist_summonees:
                if not isinstance(maillist, str) or not maillist.strip():
                    raise ValueError("Все элементы maillist_summonees должны быть непустыми строками")

        if markup_type is not None and not isinstance(markup_type, str):
            raise ValueError("markup_type должен быть строкой")

        self.logger.info(f"Создание комментария для задачи: {issue_id}")

        endpoint = f'/issues/{issue_id}/comments'

        # Формирование тела запроса
        payload = {
            "text": text
        }

        if attachment_ids is not None:
            payload["attachmentIds"] = attachment_ids

        if summonees is not None:
            payload["summonees"] = summonees

        if maillist_summonees is not None:
            payload["maillistSummonees"] = maillist_summonees

        if markup_type is not None:
            payload["markupType"] = markup_type

        self.logger.debug(f"Параметры создания комментария - Body: {len(payload)} полей")

        # Логируем дополнительную информацию
        if summonees:
            self.logger.debug(f"Призванных пользователей: {len(summonees)}")

        if maillist_summonees:
            self.logger.debug(f"Призванных рассылок: {len(maillist_summonees)}")

        if attachment_ids:
            self.logger.debug(f"Вложений: {len(attachment_ids)}")

        if markup_type:
            self.logger.debug(f"Тип разметки: {markup_type}")

        result = await self._request(endpoint, 'POST', data=payload)

        # Логируем успешное создание
        comment_id = result.get('id', 'N/A')
        author = result.get('createdBy', {}).get('display', 'N/A')
        created_date = result.get('createdAt', 'N/A')

        self.logger.info(f"Комментарий {comment_id} успешно создан для задачи {issue_id}")
        self.logger.debug(f"Автор: {author}, дата: {created_date}")

        return result