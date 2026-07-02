"""Boss Fight API tests — implement all TODO test functions."""
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from rpg.api.main import app
from rpg.api.dependencies import get_session_repo
from rpg.repositories import SessionRepository


@pytest.fixture
def client(tmp_path) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_session_repo] = lambda: SessionRepository(tmp_path)
    yield TestClient(app)
    app.dependency_overrides.clear()


# TODO: test_health_returns_ok
# Send GET /health, assert status == 200, assert body == {"status": "ok", "version": "1.0"}
def test_health_returns_ok(client: TestClient) -> None:
    raise NotImplementedError


# TODO: test_monsters_returns_list
# Send GET /monsters, assert status == 200, assert response is a non-empty list
def test_monsters_returns_list(client: TestClient) -> None:
    raise NotImplementedError


# TODO: test_hero_classes_returns_list
# Send GET /heroes/classes, assert status == 200, assert response is a non-empty list of strings
def test_hero_classes_returns_list(client: TestClient) -> None:
    raise NotImplementedError


# TODO: test_simulate_returns_winner
# Send POST /battle/simulate with {"hero_name": "Ada", "hero_class": "warrior", "monster_name": "Goblin"}
# Assert status == 200, assert "winner" key is in response JSON
def test_simulate_returns_winner(client: TestClient) -> None:
    raise NotImplementedError


# TODO: test_simulate_unknown_monster_returns_404
# Send POST /battle/simulate with a monster_name that does not exist
# Assert status == 404
def test_simulate_unknown_monster_returns_404(client: TestClient) -> None:
    raise NotImplementedError


# TODO: test_session_round_trip
# 1. POST /sessions with valid battle request → assert status == 201, get session_id from body
# 2. GET /sessions/{session_id} → assert status == 200, assert "winner" in body
def test_session_round_trip(client: TestClient) -> None:
    raise NotImplementedError


# TODO: test_session_not_found_returns_404
# Send GET /sessions/nonexistent-id → assert status == 404
def test_session_not_found_returns_404(client: TestClient) -> None:
    raise NotImplementedError


# TODO: test_report_returns_markdown
# 1. POST /sessions with valid battle request → get session_id
# 2. GET /reports/{session_id} → assert status == 200, assert "##" in response text
def test_report_returns_markdown(client: TestClient) -> None:
    raise NotImplementedError
