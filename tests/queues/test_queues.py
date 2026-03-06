"""Тест модуля queues (очереди)."""

import time
import random
import pytest

pytestmark = pytest.mark.integration

TEST_QUEUE = 'DEV'


async def test_queues_list_and_get(ctx):
    client = ctx.client

    # Список очередей
    queues = await client.queues.list()
    assert isinstance(queues, list)
    assert len(queues) > 0

    # Получение конкретной очереди
    queue = await client.queues.get(TEST_QUEUE)
    assert queue.get('key') == TEST_QUEUE

    # С expand
    queue_full = await client.queues.get(TEST_QUEUE, expand='all')
    assert 'key' in queue_full


async def test_queues_versions(ctx):
    client = ctx.client

    versions = await client.queues.versions.list(TEST_QUEUE)
    assert isinstance(versions, list)

    new_version = await client.queues.versions.create(
        queue=TEST_QUEUE,
        name="Test Version API",
        description="Тестовая версия из API"
    )
    assert new_version.get('id')
    assert new_version.get('name') == "Test Version API"


async def test_queues_fields(ctx):
    fields = await ctx.client.queues.fields.list(TEST_QUEUE)
    assert isinstance(fields, list)


async def test_queues_tags(ctx):
    client = ctx.client

    tags = await client.queues.tags.list(TEST_QUEUE)
    assert isinstance(tags, list)

    # Создать задачу с тегом, убрать тег, удалить тег
    test_tag = f"test_tag_{int(time.time())}"
    issue = await ctx.create_issue(
        queue=TEST_QUEUE,
        summary="Задача для теста тегов",
        tags=[test_tag]
    )
    issue_key = issue.get('key')

    await client.issues.update(issue_key, tags=[])
    await client.queues.tags.delete(TEST_QUEUE, test_tag)


async def test_queues_create_delete_restore(ctx):
    client = ctx.client

    q_suffix = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    q_key = f'TQ{q_suffix}'

    new_queue = await client.queues.create(
        key=q_key,
        name='Test Queue API',
        lead='1130000064986264',
        default_type='task',
        default_priority='normal',
        issue_types_config=[
            {'issueType': 'task', 'workflow': 'W4', 'resolutions': ['wontFix']}
        ],
        description='Тестовая очередь из API'
    )
    new_queue_key = new_queue.get('key', q_key)
    assert new_queue_key

    # Удаление
    await client.queues.delete(new_queue_key)

    # Восстановление
    restored = await client.queues.restore(new_queue_key)
    assert restored.get('key') == new_queue_key

    # Повторное удаление
    await client.queues.delete(new_queue_key)
