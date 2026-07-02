# level_6_api/missions/08_openapi_and_api_polish/task/tests/test_api.py
"""Pre-built API tests — provided as-is, do not modify.

These tests were written in Mission 07. They verify the app still works after
you add OpenAPI metadata in Mission 08. Run them with:

    uv run pytest task/tests/test_api.py -q
"""
import pytest
from fastapi.testclient import TestClient

from task.main import app
from task.dependencies import get_session_repo
from task.rpg.repositories import SessionRepository


@pytest.fixture
def client(tmp_path):
    """TestClient with an isolated session repository."""
    app.dependency_overrides[get_session_repo] = lambda: SessionRepository(tmp_path)
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_monsters_returns_list(client: TestClient) -> None:
    response = client.get("/monsters")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]


def test_simulate_battle(client: TestClient) -> None:
    response = client.post(
        "/battle/simulate",
        json={"hero_name": "Ada", "hero_class": "warrior", "monster_name": "Goblin"},
    )
    assert response.status_code == 200
    assert "winner" in response.json()


def test_simulate_battle_invalid_monster(client: TestClient) -> None:
    response = client.post(
        "/battle/simulate",
        json={"hero_name": "Ada", "hero_class": "warrior", "monster_name": "FakeMonster"},
    )
    assert response.status_code == 404


def test_post_session_then_get(client: TestClient) -> None:
    post_resp = client.post(
        "/sessions",
        json={"hero_name": "Ada", "hero_class": "warrior", "monster_name": "Goblin"},
    )
    assert post_resp.status_code == 201
    session_id = post_resp.json()["session_id"]
    get_resp = client.get(f"/sessions/{session_id}")
    assert get_resp.status_code == 200
    assert "winner" in get_resp.json()


def test_get_session_not_found(client: TestClient) -> None:
    response = client.get("/sessions/nonexistent")
    assert response.status_code == 404
