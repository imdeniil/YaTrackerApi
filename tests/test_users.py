"""Тест модуля users (пользователи)."""

import pytest

pytestmark = pytest.mark.integration


async def test_users(ctx):
    client = ctx.client

    # 1. Получить информацию о текущем пользователе
    myself = await client.users.get_myself()
    assert myself.get('display')
    assert myself.get('login')
    assert myself.get('uid')

    # С expand=groups
    myself_groups = await client.users.get_myself(expand="groups")
    groups = myself_groups.get('groups', [])
    assert isinstance(groups, list)

    # 2. Получить информацию о заданном пользователе
    uid = myself.get('uid')
    user = await client.users.get(uid)
    assert user.get('display') == myself.get('display')

    login = myself.get('login')
    user = await client.users.get(login)
    assert user.get('uid') == uid

    user = await client.users.get(uid, expand="groups")
    assert 'groups' in user

    # 3. Получить информацию о пользователях
    users = await client.users.list()
    assert isinstance(users, list)
    assert len(users) > 0

    # С perPage
    page1 = await client.users.list(per_page=2)
    assert isinstance(page1, list)
    assert len(page1) <= 2

    if len(page1) == 2:
        last_uid = page1[-1].get('uid')
        page2 = await client.users.list(per_page=2, id=last_uid)
        assert isinstance(page2, list)

    # Фильтр по email
    if myself.get('email'):
        by_email = await client.users.list(email=myself['email'])
        assert isinstance(by_email, list)
        assert len(by_email) >= 1

    # 4. Пользователи с относительной пагинацией
    result = await client.users.get_paginated(per_page=2)
    assert isinstance(result, dict)
    users_list = result.get('users', [])
    assert isinstance(users_list, list)
