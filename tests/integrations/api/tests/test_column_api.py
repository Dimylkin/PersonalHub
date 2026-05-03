import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def create_board(client: AsyncClient) -> dict:
    response = await client.post("/api/boards", json={"workspace": "work"})
    assert response.status_code == 201
    return response.json()


async def test_create_column_success(client: AsyncClient):
    board = await create_board(client)

    response = await client.post(
        "/api/columns",
        json={"board_id": board["id"], "type": "backlog", "order": 0},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["board_id"] == board["id"]
    assert data["type"] == "backlog"
    assert data["order"] == 0


async def test_get_all_columns_success(client: AsyncClient):
    board = await create_board(client)

    await client.post("/api/columns", json={"board_id": board["id"], "type": "backlog", "order": 0})
    await client.post("/api/columns", json={"board_id": board["id"], "type": "done", "order": 1})

    response = await client.get("/api/columns")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["type"] == "backlog"
    assert data[1]["type"] == "done"


async def test_get_column_by_id_not_found(client: AsyncClient):
    response = await client.get("/api/columns/999")

    assert response.status_code == 404
    assert response.json()["code"] == "OBJECT_NOT_FOUND"


async def test_update_column_success(client: AsyncClient):
    board = await create_board(client)
    create_response = await client.post(
        "/api/columns",
        json={"board_id": board["id"], "type": "backlog", "order": 0},
    )
    column_id = create_response.json()["id"]

    response = await client.patch(
        f"/api/columns/{column_id}",
        json={"type": "review", "order": 1},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == column_id
    assert data["type"] == "review"
    assert data["order"] == 1


async def test_delete_column_success(client: AsyncClient):
    board = await create_board(client)
    create_response = await client.post(
        "/api/columns",
        json={"board_id": board["id"], "type": "backlog", "order": 0},
    )
    column_id = create_response.json()["id"]

    response = await client.delete(f"/api/columns/{column_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = await client.get(f"/api/columns/{column_id}")
    assert get_response.status_code == 404
