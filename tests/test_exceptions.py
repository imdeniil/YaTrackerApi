"""Тест обработки ошибок (исключения)."""

import pytest

from YaTrackerApi import TrackerAPIError, NotFoundError

pytestmark = pytest.mark.integration


async def test_not_found_issue(ctx):
    """404 — задача не найдена."""
    with pytest.raises(NotFoundError) as exc_info:
        await ctx.client.issues.get("NONEXISTENT-99999")
    assert exc_info.value.status_code == 404


async def test_not_found_user(ctx):
    """404 — пользователь не найден."""
    with pytest.raises(NotFoundError) as exc_info:
        await ctx.client.users.get("nonexistent_user_xyz_123")
    assert exc_info.value.status_code == 404


async def test_catch_base_class(ctx):
    """NotFoundError ловится через базовый TrackerAPIError."""
    with pytest.raises(TrackerAPIError) as exc_info:
        await ctx.client.issues.get("NONEXISTENT-99999")
    assert isinstance(exc_info.value, NotFoundError)
    assert exc_info.value.status_code == 404


async def test_exception_attributes(ctx):
    """Проверка атрибутов исключения."""
    with pytest.raises(TrackerAPIError) as exc_info:
        await ctx.client.issues.get("NONEXISTENT-99999")
    e = exc_info.value
    assert e.status_code == 404
    assert 'NONEXISTENT-99999' in e.url
    assert e.method == 'GET'
    assert isinstance(e.errors, dict)
    assert isinstance(e.error_messages, list)


async def test_successful_request(ctx):
    """Успешный запрос — нет исключений."""
    myself = await ctx.client.users.get_myself()
    assert myself.get('display')
