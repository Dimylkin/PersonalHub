import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def create_board(client: AsyncClient) -> dict:
    response = await client.post("/api/boards", json={"workspace": "work"})
    assert response.status_code == 201
    return response.json()


async def create_column(client: AsyncClient) -> dict:
    board = await create_board(client)
    response = await client.post(
        "/api/columns",
        json={"board_id": board["id"], "type": "backlog", "order": 0},
    )
    assert response.status_code == 201
    return response.json()


async def test_create_task_success(client: AsyncClient):
    column = await create_column(client)

    response = await client.post(
        "/api/tasks",
        json={
            "column_id": column["id"],
            "title": "abc",
            "description": "abc",
            "urgency": "low",
            "order": 0,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data["id"], int)
    assert data["id"] > 0
    assert data["column_id"] == column["id"]
    assert data["title"] == "abc"
    assert data["description"] == "abc"
    assert data["urgency"] == "low"
    assert data["order"] == 0


async def test_get_all_tasks_success(client: AsyncClient):
    column = await create_column(client)

    await client.post(
        "/api/tasks",
        json={"column_id": column["id"], "title": "abc", "urgency": "low", "order": 0},
    )
    await client.post(
        "/api/tasks",
        json={"column_id": column["id"], "title": "abc", "urgency": "high", "order": 1},
    )

    response = await client.get("/api/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_task_by_id_not_found(client: AsyncClient):
    response = await client.get("/api/tasks/999")

    assert response.status_code == 404
    assert response.json()["code"] == "OBJECT_NOT_FOUND"


async def test_update_task_success(client: AsyncClient):
    column = await create_column(client)
    create_response = await client.post(
        "/api/tasks",
        json={"column_id": column["id"], "title": "abc", "urgency": "low", "order": 0},
    )
    task_id = create_response.json()["id"]

    response = await client.patch(
        f"/api/tasks/{task_id}",
        json={"title": "abc", "urgency": "critical", "order": 1},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["urgency"] == "critical"
    assert data["order"] == 1


async def test_delete_task_success(client: AsyncClient):
    column = await create_column(client)
    create_response = await client.post(
        "/api/tasks",
        json={"column_id": column["id"], "title": "abc", "urgency": "low", "order": 0},
    )
    task_id = create_response.json()["id"]

    response = await client.delete(f"/api/tasks/{task_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = await client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404
