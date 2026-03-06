"""Тест модуля dashboards (дашборды и виджеты)."""

import pytest

pytestmark = pytest.mark.integration


async def test_dashboards(ctx):
    client = ctx.client

    # 1. Создать дашборд
    dashboard = await client.dashboards.create(
        name="Test Dashboard API",
        layout="two-columns"
    )
    dashboard_id = dashboard.get('id')
    assert dashboard_id
    assert dashboard.get('name') == "Test Dashboard API"
    assert dashboard.get('layout') == "two-columns"

    # 2. Создать виджет «Время цикла»
    widget = await client.dashboards.create_cycle_time_widget(
        dashboard_id=dashboard_id,
        description="Cycle Time - DEV Queue",
        query='Queue: DEV',
        from_statuses=[{"key": "open"}],
        to_statuses=[{"key": "closed"}],
        bucket={"unit": "weeks", "count": 1},
        lines={
            "movingAverage": True,
            "standardDeviation": False,
            "percentile": [75, 90]
        },
        start="now()-3M",
        end="now()",
        mode="common-lines-and-points"
    )
    assert widget.get('id')
    assert widget.get('description') == "Cycle Time - DEV Queue"
