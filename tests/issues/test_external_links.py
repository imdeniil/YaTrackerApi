"""Тест модуля external_links (внешние связи)."""

import pytest

pytestmark = pytest.mark.integration

TEST_QUEUE = 'DEV'


async def test_external_links(ctx):
    client = ctx.client

    # Получить список приложений
    apps = await client.external.links.get_applications()
    assert isinstance(apps, list)
    assert len(apps) > 0

    # Создать задачу
    issue = await ctx.create_issue(queue=TEST_QUEUE, summary="Задача для теста внешних связей")
    issue_key = issue['key']

    # Получить связи (пустой список)
    links = await client.external.links.list(issue_key)
    assert isinstance(links, list)
    assert len(links) == 0

    # Найти приложение для связи
    app_id = None
    for app in apps:
        if app.get('id') != 'ru.yandex.messenger':
            app_id = app.get('id')
            break
    if not app_id:
        pytest.skip("Нет подходящего внешнего приложения")

    # Добавить связь
    link = await client.external.links.create(
        issue_id=issue_key,
        relationship="RELATES",
        key="EXT-TEST-001",
        origin=app_id
    )
    link_id = link.get('id')
    assert link_id

    # Проверить что появилась
    links = await client.external.links.list(issue_key)
    assert len(links) == 1

    # Удалить связь
    await client.external.links.delete(issue_key, link_id)

    # Проверить что удалена
    links = await client.external.links.list(issue_key)
    assert len(links) == 0
