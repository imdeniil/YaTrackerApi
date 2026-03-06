"""Тест модуля automations (автоматизации: автодействия, триггеры, макросы)."""

import pytest

pytestmark = pytest.mark.integration

TEST_QUEUE = 'DEV'


async def test_macros(ctx):
    client = ctx.client

    # Получить все макросы
    macros = await client.automations.macros.list(TEST_QUEUE)
    assert isinstance(macros, list)

    # Создать макрос
    new_macro = await client.automations.macros.create(
        queue=TEST_QUEUE,
        name="Test Macro API",
        body="Комментарий от макроса {{currentUser}}",
        issue_update={"tags": {"add": "macro-test"}}
    )
    macro_id = new_macro.get('id')
    assert macro_id
    assert new_macro.get('name') == "Test Macro API"

    # Получить макрос
    macro = await client.automations.macros.get(TEST_QUEUE, macro_id)
    assert macro.get('name') == "Test Macro API"

    # Редактировать макрос
    updated_macro = await client.automations.macros.update(
        queue=TEST_QUEUE,
        macro_id=macro_id,
        name="Test Macro API Updated",
        body="Обновленный комментарий {{currentDateTime}}"
    )
    assert updated_macro.get('name') == "Test Macro API Updated"

    # Удалить макрос
    await client.automations.macros.delete(TEST_QUEUE, macro_id)


async def test_autoactions(ctx):
    client = ctx.client

    # Создать автодействие
    new_autoaction = await client.automations.autoactions.create(
        queue=TEST_QUEUE,
        name="Test Autoaction API",
        filter={"priority": ["critical"]},
        actions=[{"type": "Transition", "status": {"key": "needInfo"}}],
        active=False,
        enable_notifications=False
    )
    autoaction_id = new_autoaction.get('id')
    assert autoaction_id

    # Получить параметры
    autoaction = await client.automations.autoactions.get(TEST_QUEUE, autoaction_id)
    assert autoaction.get('name') == "Test Autoaction API"
    assert autoaction.get('active') is False

    # Логи
    logs = await client.automations.autoactions.get_logs(TEST_QUEUE, autoaction_id)
    assert isinstance(logs, list)


async def test_triggers(ctx):
    client = ctx.client

    # Создать триггер
    new_trigger = await client.automations.triggers.create(
        queue=TEST_QUEUE,
        name="Test Trigger API",
        actions=[{"type": "CreateComment", "text": "Триггер: {{issue.key}}", "fromRobot": True}],
        conditions=[{"type": "Event.create"}],
        active=False
    )
    trigger_id = new_trigger.get('id')
    assert trigger_id

    # Получить параметры
    trigger = await client.automations.triggers.get(TEST_QUEUE, trigger_id)
    assert trigger.get('name') == "Test Trigger API"

    # Изменить триггер
    updated_trigger = await client.automations.triggers.update(
        queue=TEST_QUEUE,
        trigger_id=trigger_id,
        name="Test Trigger API Updated",
        actions=[{"type": "CreateComment", "text": "Обновлённый: {{issue.key}}", "fromRobot": True}]
    )
    assert updated_trigger.get('name') == "Test Trigger API Updated"

    # Логи
    trigger_logs = await client.automations.triggers.get_logs(TEST_QUEUE, trigger_id, limit=5)
    assert isinstance(trigger_logs, list)

    # Деактивировать
    await client.automations.triggers.update(TEST_QUEUE, trigger_id, active=False)
