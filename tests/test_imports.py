"""Тест модуля imports (импорт задач, комментариев, связей, файлов)."""

import pytest

pytestmark = pytest.mark.integration

USER_ID = '1130000064986264'
TEST_QUEUE = 'DEV'


async def test_import_issue(ctx):
    client = ctx.client

    imported = await client.imports.issue(
        queue=TEST_QUEUE,
        summary="Импортированная задача из API",
        created_at="2025-01-15T10:00:00.000+0300",
        created_by=USER_ID,
        description="Задача импортирована через API",
        tags=["imported", "test"],
        story_points=3.0
    )
    assert imported.get('key')
    assert imported.get('tags') == ["imported", "test"]


async def test_import_comment(ctx):
    client = ctx.client

    imported = await client.imports.issue(
        queue=TEST_QUEUE,
        summary="Задача для импорта комментария",
        created_at="2025-01-15T07:00:00.000+0000",
        created_by=USER_ID
    )
    issue_key = imported['key']

    comment = await client.imports.comment(
        issue_id=issue_key,
        text="Импортированный комментарий",
        created_at="2025-01-15T07:00:00.000+0000",
        created_by=USER_ID
    )
    assert comment.get('id')
    assert comment.get('text') == "Импортированный комментарий"


async def test_import_link(ctx):
    client = ctx.client

    issue1 = await client.imports.issue(
        queue=TEST_QUEUE,
        summary="Задача 1 для связи",
        created_at="2025-01-15T07:00:00.000+0000",
        created_by=USER_ID
    )
    issue2 = await client.imports.issue(
        queue=TEST_QUEUE,
        summary="Задача 2 для связи",
        created_at="2025-01-15T07:00:00.000+0000",
        created_by=USER_ID
    )

    link = await client.imports.link(
        issue_id=issue1['key'],
        relationship="relates",
        issue=issue2['key'],
        created_at="2025-01-15T07:00:00.000+0000",
        created_by=USER_ID
    )
    assert link.get('id')


async def test_import_file(ctx):
    client = ctx.client

    imported = await client.imports.issue(
        queue=TEST_QUEUE,
        summary="Задача для импорта файла",
        created_at="2025-01-15T07:00:00.000+0000",
        created_by=USER_ID
    )
    issue_key = imported['key']

    attachment = await client.imports.file(
        issue_id=issue_key,
        file_data=b"Imported file content from API test",
        filename="imported_file.txt",
        created_at="2025-01-15T07:00:00.000+0000",
        created_by=USER_ID
    )
    assert attachment.get('id')
    assert attachment.get('name') == "imported_file.txt"
