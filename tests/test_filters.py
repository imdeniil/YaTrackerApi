"""Тест модуля filters (фильтры/сохранённые запросы)."""

import time
import pytest

pytestmark = pytest.mark.integration

TEST_QUEUE = 'DEV'


async def test_create_filter_with_filter(ctx):
    suffix = str(int(time.time()))[-6:]
    f1 = await ctx.create_filter(
        name=f"Тестовый фильтр {suffix}",
        filter={"queue": TEST_QUEUE}
    )
    assert f1.get('id')
    assert f1.get('filter', {}).get('queue') == TEST_QUEUE


async def test_create_filter_with_query(ctx):
    suffix = str(int(time.time()))[-6:]
    f2 = await ctx.create_filter(
        name=f"Фильтр query {suffix}",
        query=f"Queue: {TEST_QUEUE}"
    )
    assert f2.get('id')
    assert TEST_QUEUE in f2.get('query', '')


async def test_get_filter(ctx):
    suffix = str(int(time.time()))[-6:]
    created = await ctx.create_filter(
        name=f"Фильтр для get {suffix}",
        filter={"queue": TEST_QUEUE}
    )
    fetched = await ctx.client.filters.get(created['id'])
    assert fetched.get('id') == created['id']
    assert fetched.get('name') == created.get('name')


async def test_update_filter(ctx):
    suffix = str(int(time.time()))[-6:]
    created = await ctx.create_filter(
        name=f"Фильтр для update {suffix}",
        filter={"queue": TEST_QUEUE}
    )
    updated = await ctx.client.filters.update(
        created['id'],
        name=f"Обновлённый фильтр {suffix}",
        query=f"Queue: {TEST_QUEUE} Status: open"
    )
    assert updated.get('name') == f"Обновлённый фильтр {suffix}"


async def test_create_filter_with_sorts_and_fields(ctx):
    suffix = str(int(time.time()))[-6:]
    f3 = await ctx.create_filter(
        name=f"Фильтр с сортировкой {suffix}",
        filter={"queue": TEST_QUEUE},
        fields=["summary", "status", "assignee"],
        sorts=[{"field": "created", "isAscending": False}]
    )
    assert f3.get('id')
    assert f3.get('fields')
    assert f3.get('sorts')
