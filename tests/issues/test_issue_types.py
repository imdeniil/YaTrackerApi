"""Тест модуля issue_types (типы задач, статусы, резолюции, приоритеты)."""

import time
import pytest

pytestmark = pytest.mark.integration


async def test_issue_types(ctx):
    client = ctx.client
    suffix = str(int(time.time()))[-6:]

    # Получить список
    types = await client.issues.types.list()
    assert isinstance(types, list)
    assert len(types) > 0

    # Создать
    type_key = f"testType{suffix}"
    new_type = await client.issues.types.create(
        key=type_key, name={"ru": "Тестовый тип", "en": "Test Type"}
    )
    if isinstance(new_type, list) and new_type:
        new_type = new_type[0]
    type_id = new_type.get('id')
    assert type_id

    # Редактировать
    updated = await client.issues.types.update(
        id_or_key=type_id,
        version=new_type.get('version'),
        name={"ru": "Обновленный тип", "en": "Updated Type"}
    )
    if isinstance(updated, list) and updated:
        updated = updated[0]
    assert updated.get('name')


async def test_statuses(ctx):
    client = ctx.client
    suffix = str(int(time.time()))[-6:]

    statuses = await client.issues.statuses.list()
    assert isinstance(statuses, list)
    assert len(statuses) > 0

    status_key = f"testStatus{suffix}"
    new_status = await client.issues.statuses.create(
        key=status_key,
        name={"ru": "Тестовый статус", "en": "Test Status"},
        type="inProgress"
    )
    if isinstance(new_status, list) and new_status:
        new_status = new_status[0]
    assert new_status.get('id')

    updated = await client.issues.statuses.update(
        id_or_key=new_status.get('id'),
        version=new_status.get('version'),
        name={"ru": "Обновленный статус", "en": "Updated Status"}
    )
    if isinstance(updated, list) and updated:
        updated = updated[0]
    assert updated.get('name')


async def test_resolutions(ctx):
    client = ctx.client
    suffix = str(int(time.time()))[-6:]

    resolutions = await client.issues.resolutions.list()
    assert isinstance(resolutions, list)
    assert len(resolutions) > 0

    res_key = f"testRes{suffix}"
    new_res = await client.issues.resolutions.create(
        key=res_key,
        name={"ru": "Тестовая резолюция", "en": "Test Resolution"}
    )
    if isinstance(new_res, list) and new_res:
        new_res = new_res[0]
    assert new_res.get('id')

    updated = await client.issues.resolutions.update(
        id_or_key=new_res.get('id'),
        version=new_res.get('version'),
        name={"ru": "Обновленная резолюция", "en": "Updated Resolution"}
    )
    if isinstance(updated, list) and updated:
        updated = updated[0]
    assert updated.get('name')


async def test_priorities(ctx):
    client = ctx.client
    suffix = str(int(time.time()))[-6:]

    priorities = await client.issues.priorities.list()
    assert isinstance(priorities, list)
    assert len(priorities) > 0

    prio_key = f"testPrio{suffix}"
    new_prio = await client.issues.priorities.create(
        key=prio_key,
        name={"ru": "Тестовый приоритет", "en": "Test Priority"},
        order=100
    )
    if isinstance(new_prio, list) and new_prio:
        new_prio = new_prio[0]
    assert new_prio.get('id')

    updated = await client.issues.priorities.update(
        id_or_key=new_prio.get('id'),
        version=new_prio.get('version'),
        name={"ru": "Обновленный приоритет", "en": "Updated Priority"}
    )
    if isinstance(updated, list) and updated:
        updated = updated[0]
    assert updated.get('name')
