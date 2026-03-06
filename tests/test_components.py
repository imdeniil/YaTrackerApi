"""Тест модуля components (компоненты)."""

import pytest

pytestmark = pytest.mark.integration


async def test_components(ctx):
    client = ctx.client
    TEST_QUEUE = 'DEV'

    # 1. Получить список компонентов
    components = await client.components.list()
    assert isinstance(components, list)

    # 2. Создать компонент
    new_component = await client.components.create(
        name="Test Component API",
        queue=TEST_QUEUE,
        description="Тестовый компонент из API",
        assign_auto=False
    )
    component_id = new_component.get('id')
    assert component_id
    assert new_component.get('name') == "Test Component API"

    # 3. Редактировать компонент
    updated = await client.components.update(
        component_id=component_id,
        version=new_component.get('version'),
        name="Test Component API Updated",
        description="Обновленное описание"
    )
    assert updated.get('name') == "Test Component API Updated"

    # 4. Права доступа пользователя
    user_perms = await client.components.permissions.get_user(
        component_id=component_id,
        user_id='1130000064986264'
    )
    assert isinstance(user_perms, dict)

    # 5. Права доступа группы
    group_perms = await client.components.permissions.get_group(
        component_id=component_id,
        group_id='1'
    )
    assert isinstance(group_perms, dict)
