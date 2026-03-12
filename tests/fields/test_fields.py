"""Тест модуля fields (глобальные и локальные поля задач)."""

import time
import pytest

pytestmark = pytest.mark.integration

TEST_QUEUE = 'DEV'


async def test_global_fields_list(ctx):
    fields = await ctx.client.issues.fields.list()
    assert isinstance(fields, list)
    assert len(fields) > 0


async def test_global_fields_get(ctx):
    fields = await ctx.client.issues.fields.list()
    assert fields
    field_id = fields[0].get('id')
    field = await ctx.client.issues.fields.get(field_id)
    assert field.get('id') == field_id


async def test_categories_list(ctx):
    """Получение списка категорий полей с их ID."""
    categories = await ctx.client.issues.fields.categories.list()
    assert isinstance(categories, list)
    assert len(categories) > 0
    # Каждая категория должна содержать id и name
    for cat in categories:
        assert 'id' in cat, f"Категория без id: {cat}"
        assert 'name' in cat, f"Категория без name: {cat}"


async def test_categories_create_and_update(ctx):
    client = ctx.client
    suffix = str(int(time.time()))[-6:]

    # Создать категорию
    category = await client.issues.fields.categories.create(
        name={"ru": f"Тестовая категория {suffix}", "en": f"Test Category {suffix}"},
        order=900
    )
    category_id = category.get('id')
    assert category_id

    # Обновить категорию
    cat_version = str(category.get('version', '1'))
    updated_cat = await client.issues.fields.categories.update(
        category_id=category_id,
        version=cat_version,
        name={"ru": f"Обновлённая категория {suffix}", "en": f"Updated Category {suffix}"}
    )
    assert updated_cat.get('name')


async def test_create_global_field(ctx):
    client = ctx.client
    suffix = str(int(time.time()))[-6:]

    # Сначала создаём категорию
    category = await client.issues.fields.categories.create(
        name={"ru": f"Категория для поля {suffix}", "en": f"Field Category {suffix}"},
        order=901
    )
    category_id = category.get('id')

    # Создать глобальное поле
    field_key = f"testField{suffix}"
    new_field = await client.issues.fields.create(
        name={"ru": f"Тестовое поле {suffix}", "en": f"Test Field {suffix}"},
        id=field_key,
        category=category_id,
        type="ru.yandex.startrek.core.fields.StringFieldType"
    )
    assert new_field.get('id') == field_key


async def test_local_fields(ctx):
    client = ctx.client

    # Список
    local_fields = await client.issues.fields.local.list(TEST_QUEUE)
    assert isinstance(local_fields, list)

    # Получить конкретное (если есть)
    if local_fields:
        local_key = local_fields[0].get('key') or local_fields[0].get('id')
        if local_key:
            local_field = await client.issues.fields.local.get(TEST_QUEUE, local_key)
            assert local_field.get('id')


async def test_create_local_field(ctx):
    client = ctx.client
    suffix = str(int(time.time()))[-6:]

    # Создаём категорию
    category = await client.issues.fields.categories.create(
        name={"ru": f"Категория для лок. поля {suffix}", "en": f"Local Field Cat {suffix}"},
        order=902
    )
    category_id = category.get('id')

    # Создать локальное поле
    local_field_key = f"localTestField{suffix}"
    new_local = await client.issues.fields.local.create(
        queue_id=TEST_QUEUE,
        name={"ru": f"Локальное тестовое {suffix}", "en": f"Local Test {suffix}"},
        id=local_field_key,
        category=category_id,
        type="ru.yandex.startrek.core.fields.StringFieldType"
    )
    assert new_local.get('id')
