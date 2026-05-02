import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def test_create_board_success(client: AsyncClient):
    response = await client.post(
        "/api/boards",
        json={
            "workspace": "work",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["workspace"] == "work"


async def test_get_all_boards_empty(client: AsyncClient):
    response = await client.get("/api/boards")

    assert response.status_code == 200
    assert response.json() == []


async def test_get_all_boards_success(client: AsyncClient):
    await client.post("/api/boards", json={"workspace": "work"})
    await client.post("/api/boards", json={"workspace": "study"})

    response = await client.get("/api/boards")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["workspace"] == "work"
    assert data[1]["workspace"] == "study"


async def test_get_board_by_id_success(client: AsyncClient):
    create_response = await client.post(
        "/api/boards",
        json={"workspace": "life"},
    )

    board_id = create_response.json()["id"]

    response = await client.get(f"/api/boards/{board_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == board_id
    assert data["workspace"] == "life"


async def test_get_board_by_id_not_found(client: AsyncClient):
    response = await client.get("/api/boards/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Board not found"


async def test_create_board_invalid_workspace(client: AsyncClient):
    response = await client.post(
        "/api/boards",
        json={"workspace": "INVALID"},
    )

    assert response.status_code == 422


async def test_create_board_empty_body(client: AsyncClient):
    response = await client.post("/api/boards", json={})

    assert response.status_code == 422


async def test_update_board_success(client: AsyncClient):
    create_response = await client.post(
        "/api/boards",
        json={"workspace": "work"},
    )

    board_id = create_response.json()["id"]

    response = await client.patch(
        f"/api/boards/{board_id}",
        json={"workspace": "study"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == board_id
    assert data["workspace"] == "study"


async def test_update_board_not_found(client: AsyncClient):
    response = await client.patch(
        "/api/boards/999",
        json={"workspace": "life"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Board not found"


async def test_update_board_invalid_workspace(client: AsyncClient):
    create_response = await client.post(
        "/api/boards",
        json={"workspace": "work"},
    )

    board_id = create_response.json()["id"]

    response = await client.patch(
        f"/api/boards/{board_id}",
        json={"workspace": "INVALID"},
    )

    assert response.status_code == 422


async def test_delete_board_success(client: AsyncClient):
    create_response = await client.post(
        "/api/boards",
        json={"workspace": "work"},
    )

    board_id = create_response.json()["id"]

    response = await client.delete(f"/api/boards/{board_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = await client.get(f"/api/boards/{board_id}")

    assert get_response.status_code == 404


async def test_delete_board_not_found(client: AsyncClient):
    response = await client.delete("/api/boards/999")

    assert response.status_code in (204, 404)
