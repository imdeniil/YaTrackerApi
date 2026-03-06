"""Тест модуля issues (задачи): CRUD, поиск, подсчёт, подмодули."""

import pytest

pytestmark = pytest.mark.integration

TEST_QUEUE = 'DEV'


async def test_issues_crud(ctx):
    client = ctx.client

    # Создать задачу
    issue = await ctx.create_issue(
        queue=TEST_QUEUE,
        summary="Тестовая задача для test_issues",
        description="Описание тестовой задачи"
    )
    issue_key = issue['key']
    assert issue_key
    assert issue.get('summary') == "Тестовая задача для test_issues"

    # Получить задачу
    fetched = await client.issues.get(issue_key)
    assert fetched['key'] == issue_key

    # С expand
    fetched_expand = await client.issues.get(issue_key, expand='transitions')
    assert 'transitions' in fetched_expand

    # Редактировать
    updated = await client.issues.update(
        issue_key,
        summary="Обновлённая тестовая задача",
        description="Обновлённое описание"
    )
    assert updated.get('summary') == "Обновлённая тестовая задача"


async def test_issues_search_and_count(ctx):
    client = ctx.client

    results = await client.issues.search(filter={'queue': TEST_QUEUE}, per_page=5)
    assert isinstance(results, list)
    assert len(results) > 0

    count = await client.issues.count(filter={'queue': TEST_QUEUE})
    assert isinstance(count, int)
    assert count > 0


async def test_issues_comments(ctx):
    client = ctx.client
    issue = await ctx.create_issue(queue=TEST_QUEUE, summary="Задача для комментариев")
    issue_key = issue['key']

    comment = await ctx.add_comment(issue_key, text="Тестовый комментарий")
    comment_id = str(comment['id'])
    assert comment_id

    comments = await client.issues.comments.list(issue_key)
    assert isinstance(comments, list)
    assert len(comments) >= 1

    updated = await client.issues.comments.update(
        issue_key, comment_id, text="Обновлённый комментарий"
    )
    assert updated.get('text') == "Обновлённый комментарий"


async def test_issues_attachments(ctx):
    client = ctx.client
    issue = await ctx.create_issue(queue=TEST_QUEUE, summary="Задача для вложений")
    issue_key = issue['key']

    att = await ctx.attach_file(issue_key, b"test file content", "test_file.txt")
    att_id = str(att['id'])
    assert att_id

    attachments = await client.issues.attachments.list(issue_key)
    assert isinstance(attachments, list)
    assert len(attachments) >= 1

    data = await client.issues.attachments.download(issue_key, att_id, att['name'])
    assert len(data) > 0


async def test_issues_checklists(ctx):
    client = ctx.client
    issue = await ctx.create_issue(queue=TEST_QUEUE, summary="Задача для чеклиста")
    issue_key = issue['key']

    await ctx.add_checklist_item(issue_key, "Пункт 1")
    await ctx.add_checklist_item(issue_key, "Пункт 2")

    checklist = await client.issues.checklists.list(issue_key)
    assert isinstance(checklist, list)
    assert len(checklist) >= 2


async def test_issues_links(ctx):
    client = ctx.client
    issue1 = await ctx.create_issue(queue=TEST_QUEUE, summary="Задача 1")
    issue2 = await ctx.create_issue(queue=TEST_QUEUE, summary="Задача 2")

    link = await client.issues.links.create(issue1['key'], 'relates', issue2['key'])
    assert link.get('id')

    links = await client.issues.links.list(issue1['key'])
    assert isinstance(links, list)
    assert len(links) >= 1

    await client.issues.links.delete(issue1['key'], str(links[0]['id']))


async def test_issues_transitions(ctx):
    client = ctx.client
    issue = await ctx.create_issue(queue=TEST_QUEUE, summary="Задача для переходов")
    issue_key = issue['key']

    transitions = await client.issues.transitions.list(issue_key)
    assert isinstance(transitions, list)
    assert len(transitions) > 0
