"""Тест модуля boards (доски задач, колонки, спринты)."""

import pytest

pytestmark = pytest.mark.integration


async def test_boards_crud(ctx):
    client = ctx.client

    # Получить все доски
    boards = await client.boards.list()
    assert isinstance(boards, list)
    assert len(boards) > 0

    # Пагинация
    boards_page = await client.boards.list_paginated(per_page=5)
    assert isinstance(boards_page, list)
    assert len(boards_page) <= 5

    # Создать доску
    new_board = await client.boards.create(
        name="Test Board API",
        board_permissions_template="private",
        columns=[
            {"name": "Open", "statuses": ["open"]},
            {"name": "In Progress", "statuses": ["inProgress"]},
            {"name": "Done", "statuses": ["closed"]}
        ]
    )
    board_id = new_board.get('id')
    assert board_id
    assert new_board.get('name') == "Test Board API"

    # Получить доску
    board = await client.boards.get(board_id)
    assert board.get('name') == "Test Board API"

    # Редактировать доску
    updated_board = await client.boards.update(board_id=board_id, name="Test Board API Updated")
    assert updated_board.get('name') == "Test Board API Updated"

    # --- Колонки ---

    # Получить все колонки
    columns = await client.boards.columns.list(board_id)
    assert isinstance(columns, list)
    assert len(columns) == 3

    # Создать колонку
    new_column = await client.boards.columns.create(
        board_id=board_id, name="Review", statuses=["needInfo"]
    )
    column_id = new_column.get('id')
    assert column_id

    # Получить колонку
    column = await client.boards.columns.get(board_id, column_id)
    assert column.get('name') == "Review"

    # Редактировать колонку
    updated_column = await client.boards.columns.update(
        board_id=board_id, column_id=column_id, name="Code Review"
    )
    assert updated_column.get('name') == "Code Review"

    # Удалить колонку
    await client.boards.columns.delete(board_id, column_id)

    # --- Спринты ---

    # Включаем спринты
    await client.boards.update(board_id=board_id, backlog_available=True, sprints_available=True)

    # Создать спринт
    new_sprint = await client.boards.sprints.create(
        name="Test Sprint API",
        board_id=board_id,
        start_date="2026-04-01",
        end_date="2026-04-14"
    )
    sprint_id = new_sprint.get('id')
    assert sprint_id
    assert new_sprint.get('status') == "draft"

    # Получить все спринты
    sprints = await client.boards.sprints.list(board_id)
    assert isinstance(sprints, list)
    assert len(sprints) >= 1

    # Получить спринт
    sprint = await client.boards.sprints.get(sprint_id)
    assert sprint.get('name') == "Test Sprint API"

    # Очистка — удалить доску
    await client.boards.delete(board_id)
