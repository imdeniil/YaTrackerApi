"""Тест модуля entities (проекты, портфели, цели)."""

import pytest

pytestmark = pytest.mark.integration


async def test_entities_crud(ctx):
    client = ctx.client

    # Создание проекта
    project = await client.entities.create(
        entity_type="project",
        summary="Тест Entities API",
        description="Проект для тестирования API сущностей"
    )
    project_id = project.get('id') or project.get('shortId')
    assert project_id

    # Получение
    got = await client.entities.get(
        entity_type="project",
        entity_id=project_id,
        fields="summary,description,teamAccess"
    )
    assert got.get('fields', {}).get('summary') == "Тест Entities API"

    # Обновление
    updated = await client.entities.update(
        entity_type="project",
        entity_id=project_id,
        summary="Тест Entities API (обновлено)"
    )
    assert updated.get('id')

    # Поиск
    search_result = await client.entities.search(
        entity_type="project",
        input="Тест Entities API",
        fields="summary"
    )
    assert isinstance(search_result, (dict, int))

    # История изменений
    changelog = await client.entities.changelog(
        entity_type="project",
        entity_id=project_id,
        per_page=5
    )
    assert isinstance(changelog, dict)

    # Удаление
    await client.entities.delete(entity_type="project", entity_id=project_id)


async def test_entities_comments(ctx):
    client = ctx.client

    project = await client.entities.create(entity_type="project", summary="Проект для комментариев")
    project_id = project.get('id') or project.get('shortId')

    # Добавить комментарий
    comment = await client.entities.comments.create(
        entity_type="project", entity_id=project_id, text="Тестовый комментарий"
    )
    comment_id = str(comment.get('id'))
    assert comment_id

    # Список
    comments = await client.entities.comments.list(entity_type="project", entity_id=project_id)
    assert isinstance(comments, list)
    assert len(comments) >= 1

    # Получить один
    got = await client.entities.comments.get(
        entity_type="project", entity_id=project_id, comment_id=comment_id
    )
    assert got.get('id')

    # Редактировать
    updated = await client.entities.comments.update(
        entity_type="project", entity_id=project_id, comment_id=comment_id,
        text="Обновлённый комментарий"
    )
    assert updated.get('text') == "Обновлённый комментарий"

    # Удалить
    await client.entities.comments.delete(
        entity_type="project", entity_id=project_id, comment_id=comment_id
    )

    await client.entities.delete(entity_type="project", entity_id=project_id)


async def test_entities_checklists(ctx):
    client = ctx.client

    project = await client.entities.create(entity_type="project", summary="Проект для чеклистов")
    project_id = project.get('id') or project.get('shortId')

    # Создать пункты
    await client.entities.checklists.create(
        entity_type="project", entity_id=project_id, text="Пункт 1"
    )
    await client.entities.checklists.create(
        entity_type="project", entity_id=project_id, text="Пункт 2"
    )

    # Получить ID пунктов
    entity = await client.entities.get(
        entity_type="project", entity_id=project_id, fields="checklistItems"
    )
    items = entity.get('fields', {}).get('checklistItems', [])
    assert len(items) >= 2

    item1_id = items[0].get('id')
    item2_id = items[1].get('id')

    # Изменить
    await client.entities.checklists.item.update(
        entity_type="project", entity_id=project_id,
        checklist_item_id=item1_id, text="Пункт 1 (обновлён)", checked=True
    )

    # Переместить
    await client.entities.checklists.item.move(
        entity_type="project", entity_id=project_id,
        checklist_item_id=item2_id, before=item1_id
    )

    # Удалить пункт
    await client.entities.checklists.item.delete(
        entity_type="project", entity_id=project_id, checklist_item_id=item2_id
    )

    # Удалить чеклист
    await client.entities.checklists.delete(entity_type="project", entity_id=project_id)

    await client.entities.delete(entity_type="project", entity_id=project_id)


async def test_entities_links(ctx):
    client = ctx.client

    p1 = await client.entities.create(entity_type="project", summary="Проект 1")
    p1_id = p1.get('id') or p1.get('shortId')
    p2 = await client.entities.create(entity_type="project", summary="Проект 2")
    p2_id = p2.get('id') or p2.get('shortId')

    # Создать связь
    await client.entities.links.create(
        entity_type="project", entity_id=p1_id,
        relationship="depends on", entity=p2_id
    )

    # Получить связи
    links = await client.entities.links.get(entity_type="project", entity_id=p1_id)
    assert isinstance(links, list)
    assert len(links) >= 1

    # Удалить связь
    await client.entities.links.delete(
        entity_type="project", entity_id=p1_id, right=p2_id
    )

    await client.entities.delete(entity_type="project", entity_id=p2_id)
    await client.entities.delete(entity_type="project", entity_id=p1_id)


async def test_entities_attachments(ctx):
    client = ctx.client

    project = await client.entities.create(entity_type="project", summary="Проект для файлов")
    project_id = project.get('id') or project.get('shortId')

    # Загрузка временного файла
    temp_file = await client.issues.attachments.upload_temp(
        file_data=b"Test entity attachment content", filename="entity_test.txt"
    )
    temp_file_id = str(temp_file.get('id'))
    assert temp_file_id

    # Прикрепить
    await client.entities.attachments.attach(
        entity_type="project", entity_id=project_id, file_id=temp_file_id
    )

    # Список файлов
    files = await client.entities.attachments.list(
        entity_type="project", entity_id=project_id
    )
    assert isinstance(files, list)
    assert len(files) >= 1
    file_id = str(files[0].get('id'))

    # Информация о файле
    file_info = await client.entities.attachments.get(
        entity_type="project", entity_id=project_id, file_id=file_id
    )
    assert file_info.get('name') == "entity_test.txt"

    # Удалить файл
    await client.entities.attachments.delete(
        entity_type="project", entity_id=project_id, file_id=file_id
    )

    await client.entities.delete(entity_type="project", entity_id=project_id)


async def test_entities_settings(ctx):
    client = ctx.client

    project = await client.entities.create(entity_type="project", summary="Проект для настроек")
    project_id = project.get('id') or project.get('shortId')

    # Получить настройки
    settings = await client.entities.settings.get(
        entity_type="project", entity_id=project_id
    )
    assert isinstance(settings, dict)

    # Обновить настройки
    updated = await client.entities.settings.update(
        entity_type="project", entity_id=project_id,
        permission_sources=[]
    )
    assert isinstance(updated, dict)

    await client.entities.delete(entity_type="project", entity_id=project_id)


async def test_entities_key_results(ctx):
    client = ctx.client

    goal = await client.entities.create(entity_type="goal", summary="Тестовая цель для KR")
    goal_id = goal.get('id') or goal.get('shortId')

    # Добавить KR
    kr = await client.entities.update_key_results(
        entity_id=goal_id,
        key_result_items={"add": {"type": "binary", "text": "Запустить MVP"}}
    )
    kr_items = kr.get('fields', {}).get('keyResultItems', [])
    assert len(kr_items) >= 1

    # Очистить KR
    kr_cleared = await client.entities.update_key_results(
        entity_id=goal_id, key_result_items=None
    )
    kr_items = kr_cleared.get('fields', {}).get('keyResultItems', [])
    assert len(kr_items) == 0

    await client.entities.delete(entity_type="goal", entity_id=goal_id)


async def test_entities_metrics(ctx):
    client = ctx.client

    project = await client.entities.create(entity_type="project", summary="Проект для метрик")
    project_id = project.get('id') or project.get('shortId')

    # Добавить метрику
    result = await client.entities.update_metrics(
        entity_type="project", entity_id=project_id,
        metric_items={"add": {"text": "Тестовая метрика"}}
    )
    items = result.get('fields', {}).get('metricItems', [])
    assert len(items) >= 1

    # Удалить метрики
    cleared = await client.entities.update_metrics(
        entity_type="project", entity_id=project_id, metric_items=None
    )
    items = cleared.get('fields', {}).get('metricItems', [])
    assert len(items) == 0

    await client.entities.delete(entity_type="project", entity_id=project_id)
