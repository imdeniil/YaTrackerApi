"""
Общие фикстуры для интеграционных тестов с Yandex Tracker API.

Запуск:
    uv run pytest tests/ -m integration -v
    uv run pytest tests/issues/ -m integration -v
"""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from typing import List, Dict, Any, Optional
from YaTrackerApi import YandexTrackerClient
from env import TRACKER_API_KEY, TRACKER_ORG_ID


class TestContext:
    """Контекст тестирования с автоматической очисткой созданных сущностей."""

    def __init__(self, log_level: str = "WARNING"):
        self.client: Optional[YandexTrackerClient] = None
        self._log_level = log_level
        self._created_issues: List[str] = []
        self._created_filters: List[int] = []
        self._created_comments: List[Dict[str, str]] = []
        self._created_attachments: List[Dict[str, str]] = []
        self._issues_with_checklists: List[str] = []

    async def __aenter__(self):
        self.client = YandexTrackerClient(TRACKER_API_KEY, TRACKER_ORG_ID, log_level=self._log_level)
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._cleanup()
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)

    async def _cleanup(self):
        """Очищает все созданные в тесте сущности."""
        errors = []

        for att in self._created_attachments:
            try:
                await self.client.issues.attachments.delete(att['issue_id'], att['attachment_id'])
            except Exception as e:
                errors.append(f"attachment {att}: {e}")

        for com in self._created_comments:
            try:
                await self.client.issues.comments.delete(com['issue_id'], com['comment_id'])
            except Exception as e:
                errors.append(f"comment {com}: {e}")

        for issue_id in self._issues_with_checklists:
            try:
                await self.client.issues.checklists.delete(issue_id)
            except Exception:
                pass

        for fid in self._created_filters:
            try:
                await self.client.filters.delete(fid)
            except Exception:
                pass

        if errors:
            print(f"\n[Очистка] Ошибки: {len(errors)}")
            for e in errors:
                print(f"  - {e}")

    async def create_issue(self, **kwargs) -> Dict[str, Any]:
        """Создать задачу (отслеживается для отчёта)."""
        result = await self.client.issues.create(**kwargs)
        self._created_issues.append(result['key'])
        return result

    async def create_filter(self, **kwargs) -> Dict[str, Any]:
        """Создать фильтр (отслеживается для удаления)."""
        result = await self.client.filters.create(**kwargs)
        self._created_filters.append(result['id'])
        return result

    async def add_comment(self, issue_id: str, **kwargs) -> Dict[str, Any]:
        """Добавить комментарий (отслеживается для удаления)."""
        result = await self.client.issues.comments.create(issue_id, **kwargs)
        self._created_comments.append({
            'issue_id': issue_id,
            'comment_id': str(result['id'])
        })
        return result

    async def attach_file(self, issue_id: str, file_data: bytes,
                          filename: str, **kwargs) -> Dict[str, Any]:
        """Прикрепить файл (отслеживается для удаления)."""
        result = await self.client.issues.attachments.attach(
            issue_id, file_data, filename, **kwargs
        )
        self._created_attachments.append({
            'issue_id': issue_id,
            'attachment_id': str(result['id'])
        })
        return result

    async def add_checklist_item(self, issue_id: str, text: str, **kwargs) -> Dict[str, Any]:
        """Добавить пункт чеклиста (чеклист отслеживается для очистки)."""
        result = await self.client.issues.checklists.create(issue_id, text, **kwargs)
        if issue_id not in self._issues_with_checklists:
            self._issues_with_checklists.append(issue_id)
        return result


@pytest.fixture
async def ctx():
    """Фикстура TestContext с автоматической очисткой."""
    async with TestContext() as context:
        yield context
