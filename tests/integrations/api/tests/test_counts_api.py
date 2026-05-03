import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def create_board(client: AsyncClient, workspace: str = "work") -> dict:
    response = await client.post(
        "/api/boards",
        json={"workspace": workspace},
    )
    assert response.status_code == 201
    return response.json()


async def create_column(
    client: AsyncClient,
    board_id: int,
    column_type: str = "backlog",
    order: int = 0,
) -> dict:
    response = await client.post(
        "/api/columns",
        json={
            "board_id": board_id,
            "type": column_type,
            "order": order,
        },
    )
    assert response.status_code == 201
    return response.json()


async def create_task(
    client: AsyncClient,
    column_id: int,
    title: str = "abc",
    order: int = 0,
) -> dict:
    response = await client.post(
        "/api/tasks",
        json={
            "column_id": column_id,
            "title": title,
            "description": "abc",
            "urgency": "low",
            "order": order,
        },
    )
    assert response.status_code == 201
    return response.json()


async def test_count_tasks_by_board_id_success(client: AsyncClient):
    board = await create_board(client)
    column_1 = await create_column(client, board_id=board["id"], column_type="backlog", order=0)
    column_2 = await create_column(client, board_id=board["id"], column_type="done", order=1)

    await create_task(client, column_id=column_1["id"], title="task-1", order=0)
    await create_task(client, column_id=column_1["id"], title="task-2", order=1)
    await create_task(client, column_id=column_2["id"], title="task-3", order=0)

    response = await client.get(f"/api/boards/{board['id']}/tasks/count")

    assert response.status_code == 200
    assert response.json() == {
        "board_id": board["id"],
        "tasks_count": 3,
    }


async def test_count_tasks_by_board_id_empty_board(client: AsyncClient):
    board = await create_board(client)

    response = await client.get(f"/api/boards/{board['id']}/tasks/count")

    assert response.status_code == 200
    assert response.json() == {
        "board_id": board["id"],
        "tasks_count": 0,
    }


async def test_count_tasks_by_board_id_not_found(client: AsyncClient):
    response = await client.get("/api/boards/999/tasks/count")

    assert response.status_code == 404
    assert response.json()["code"] == "OBJECT_NOT_FOUND"
    assert response.json()["details"] == {"id": 999}


async def test_count_tasks_for_all_boards_success(client: AsyncClient):
    board_1 = await create_board(client, workspace="work")
    board_2 = await create_board(client, workspace="study")

    column_1 = await create_column(client, board_id=board_1["id"], column_type="backlog", order=0)
    column_2 = await create_column(client, board_id=board_2["id"], column_type="review", order=0)

    await create_task(client, column_id=column_1["id"], title="task-1", order=0)
    await create_task(client, column_id=column_1["id"], title="task-2", order=1)
    await create_task(client, column_id=column_2["id"], title="task-3", order=0)

    response = await client.get("/api/boards/tasks/count")

    assert response.status_code == 200

    data = sorted(response.json(), key=lambda item: item["board_id"])
    assert data == [
        {"board_id": board_1["id"], "tasks_count": 2},
        {"board_id": board_2["id"], "tasks_count": 1},
    ]


async def test_count_tasks_by_column_id_success(client: AsyncClient):
    board = await create_board(client)
    column = await create_column(client, board_id=board["id"])

    await create_task(client, column_id=column["id"], title="task-1", order=0)
    await create_task(client, column_id=column["id"], title="task-2", order=1)

    response = await client.get(f"/api/columns/{column['id']}/tasks/count")

    assert response.status_code == 200
    assert response.json() == {
        "column_id": column["id"],
        "tasks_count": 2,
    }


async def test_count_tasks_by_column_id_empty_column(client: AsyncClient):
    board = await create_board(client)
    column = await create_column(client, board_id=board["id"])

    response = await client.get(f"/api/columns/{column['id']}/tasks/count")

    assert response.status_code == 200
    assert response.json() == {
        "column_id": column["id"],
        "tasks_count": 0,
    }


async def test_count_tasks_for_all_columns_success(client: AsyncClient):
    board = await create_board(client)
    column_1 = await create_column(client, board_id=board["id"], column_type="backlog", order=0)
    column_2 = await create_column(client, board_id=board["id"], column_type="done", order=1)

    await create_task(client, column_id=column_1["id"], title="task-1", order=0)
    await create_task(client, column_id=column_1["id"], title="task-2", order=1)
    await create_task(client, column_id=column_2["id"], title="task-3", order=0)

    response = await client.get("/api/columns/tasks/count")

    assert response.status_code == 200

    data = sorted(response.json(), key=lambda item: item["column_id"])
    assert data == [
        {"column_id": column_1["id"], "tasks_count": 2},
        {"column_id": column_2["id"], "tasks_count": 1},
    ]
