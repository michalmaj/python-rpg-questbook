# level_6_api/missions/07_api_tests/task/tests/test_api.py
"""Mission 07: API Tests with TestClient.

Write at least 6 tests covering: status codes, response body fields,
404 on missing resources, and the session round-trip (POST then GET).

Rules:
  - Use the `client` fixture provided below — do NOT modify it.
  - Use `app.dependency_overrides` (already wired in the fixture) for isolation.
  - No patching or mocking — dependency_overrides is the only isolation you need.
"""
import pytest
from fastapi.testclient import TestClient

from task.main import app
from task.dependencies import get_session_repo
from task.rpg.repositories import SessionRepository


@pytest.fixture
def client(tmp_path):
    """TestClient with an isolated session repository.

    app.dependency_overrides swaps the real SessionRepository (which writes
    to data/sessions/) with a temporary one backed by tmp_path.
    Each test gets a clean, empty directory — no leftover files.
    """
    app.dependency_overrides[get_session_repo] = lambda: SessionRepository(tmp_path)
    yield TestClient(app)
    app.dependency_overrides.clear()


# ── TODO 1 ────────────────────────────────────────────────────────────────────
# Test that GET /health returns 200 with body {"status": "ok"}.
def test_health_check(client: TestClient) -> None:
    raise NotImplementedError("TODO: implement test_health_check")


# ── TODO 2 ────────────────────────────────────────────────────────────────────
# Test that GET /monsters returns 200 and a non-empty list.
# Check that the first item has a "name" key.
def test_get_monsters_returns_list(client: TestClient) -> None:
    raise NotImplementedError("TODO: implement test_get_monsters_returns_list")


# ── TODO 3 ────────────────────────────────────────────────────────────────────
# Test that POST /battle/simulate with a valid request returns 200.
# Use hero_name="Ada", hero_class="warrior", monster_name="Goblin".
# Assert "winner" is in the response JSON.
def test_simulate_battle(client: TestClient) -> None:
    raise NotImplementedError("TODO: implement test_simulate_battle")


# ── TODO 4 ────────────────────────────────────────────────────────────────────
# Test that POST /battle/simulate with an unknown monster returns 404.
# Use monster_name="FakeMonster".
def test_simulate_battle_invalid_monster(client: TestClient) -> None:
    raise NotImplementedError("TODO: implement test_simulate_battle_invalid_monster")


# ── TODO 5 ────────────────────────────────────────────────────────────────────
# Test the full session round-trip:
#   1. POST /sessions with a valid request → assert status 201
#   2. Extract "session_id" from the response JSON
#   3. GET /sessions/{session_id} → assert status 200
#   4. Assert "winner" is in the response JSON
def test_post_session_then_get(client: TestClient) -> None:
    raise NotImplementedError("TODO: implement test_post_session_then_get")


# ── TODO 6 ────────────────────────────────────────────────────────────────────
# Test that GET /sessions/nonexistent returns 404.
def test_get_session_not_found(client: TestClient) -> None:
    raise NotImplementedError("TODO: implement test_get_session_not_found")
