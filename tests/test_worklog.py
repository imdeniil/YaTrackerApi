"""Тест модуля worklog (учёт времени)."""

import pytest

pytestmark = pytest.mark.integration


async def test_worklog(ctx):
    client = ctx.client

    # Создаём задачу для тестов
    issue = await ctx.create_issue(queue='DEV', summary="Задача для теста учёта времени")
    issue_key = issue['key']

    # 1. Добавить запись о затраченном времени
    entry = await client.worklog.create(
        issue_id=issue_key,
        start="2026-03-01T10:00:00.000+0300",
        duration="PT2H30M",
        comment="Работа над задачей"
    )
    worklog_id = entry.get('id')
    assert worklog_id
    assert entry.get('duration') == "PT2H30M"

    # Вторая запись
    entry2 = await client.worklog.create(
        issue_id=issue_key,
        start="2026-03-02T14:00:00.000+0300",
        duration="PT45M",
        comment="Код ревью"
    )
    worklog_id2 = entry2.get('id')
    assert worklog_id2

    # 2. Получить все записи по задаче
    worklogs = await client.worklog.list(issue_key)
    assert isinstance(worklogs, list)
    assert len(worklogs) == 2

    # 3. Отобрать записи по параметрам
    found = await client.worklog.search(
        created_by="1130000064986264",
        created_at_from="2026-03-01T00:00:00.000+0000",
        created_at_to="2026-03-07T00:00:00.000+0000"
    )
    assert isinstance(found, list)
    assert len(found) >= 1

    # 4. Редактировать запись
    updated = await client.worklog.update(
        issue_id=issue_key,
        worklog_id=worklog_id,
        duration="PT3H",
        comment="Обновлённый комментарий"
    )
    assert updated.get('duration') == "PT3H"
    assert updated.get('comment') == "Обновлённый комментарий"

    # 5. Удалить запись
    await client.worklog.delete(issue_key, worklog_id2)
    remaining = await client.worklog.list(issue_key)
    assert len(remaining) == 1
