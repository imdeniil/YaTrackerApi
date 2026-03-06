"""Тест реструктуризации API — проверяем новые пути доступа."""

import pytest

pytestmark = pytest.mark.integration

TEST_QUEUE = 'DEV'


async def test_issues_types(ctx):
    types = await ctx.client.issues.types.list()
    assert isinstance(types, list)
    assert len(types) > 0


async def test_issues_statuses(ctx):
    statuses = await ctx.client.issues.statuses.list()
    assert isinstance(statuses, list)
    assert len(statuses) > 0


async def test_issues_resolutions(ctx):
    resolutions = await ctx.client.issues.resolutions.list()
    assert isinstance(resolutions, list)
    assert len(resolutions) > 0


async def test_issues_priorities(ctx):
    priorities = await ctx.client.issues.priorities.list()
    assert isinstance(priorities, list)
    assert len(priorities) > 0


async def test_queues_permissions(ctx):
    client = ctx.client
    myself = await client.users.get_myself()
    uid = str(myself.get('uid'))
    user_perms = await client.queues.permissions.get_user(TEST_QUEUE, uid)
    assert isinstance(user_perms, dict)


async def test_external_links_path(ctx):
    client = ctx.client

    # get_applications
    apps = await client.external.links.get_applications()
    assert isinstance(apps, list)

    # create + delete
    issue = await ctx.create_issue(queue=TEST_QUEUE, summary="Тест реструктуризации")
    issue_key = issue['key']

    links = await client.external.links.list(issue_key)
    assert isinstance(links, list)

    app_id = None
    for app in apps:
        if app.get('id') != 'ru.yandex.messenger':
            app_id = app.get('id')
            break
    if app_id:
        link = await client.external.links.create(
            issue_id=issue_key,
            relationship="RELATES",
            key="RESTRUCTURE-TEST-001",
            origin=app_id
        )
        link_id = link.get('id')
        assert link_id
        await client.external.links.delete(issue_key, link_id)
