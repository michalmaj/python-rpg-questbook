"""Boss Fight: API tests for Concurrent Tournament Runner.

Rules:
  - Use SyncWorker via app.dependency_overrides for determinism
  - No time.sleep() in tests
  - Write at least 6 tests
"""
import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.dependencies import get_job_repo, get_worker
from jobs.jobs import InMemoryJobRepository, SyncWorker


@pytest.fixture
def client():
    repo = InMemoryJobRepository()
    worker = SyncWorker(repo)
    app.dependency_overrides[get_job_repo] = lambda: repo
    app.dependency_overrides[get_worker] = lambda: worker
    yield TestClient(app, raise_server_exceptions=False)
    app.dependency_overrides.clear()


def test_post_tournaments_returns_202_with_job_id(client: TestClient) -> None:
    """Test POST /tournaments returns 202 with job_id."""
    r = client.post("/tournaments", json={"battles": 10})
    assert r.status_code == 202
    data = r.json()
    assert "job_id" in data
    assert isinstance(data["job_id"], str)
    assert len(data["job_id"]) > 0


def test_get_tournament_returns_completed_with_result(client: TestClient) -> None:
    """Test GET /tournaments/{job_id} returns completed status with result."""
    r = client.post("/tournaments", json={"battles": 10})
    job_id = r.json()["job_id"]
    r = client.get(f"/tournaments/{job_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "completed"
    assert "result" in data
    assert data["result"]["total_battles"] == 10
    assert data["result"]["hero_wins"] >= 0
    assert data["result"]["monster_wins"] >= 0


def test_get_report_returns_markdown(client: TestClient) -> None:
    """Test GET /tournaments/{job_id}/report returns Markdown text/plain."""
    r = client.post("/tournaments", json={"battles": 10})
    job_id = r.json()["job_id"]
    r = client.get(f"/tournaments/{job_id}/report")
    assert r.status_code == 200
    assert "text/plain" in r.headers.get("content-type", "")
    assert "## Tournament Report" in r.text


def test_get_nonexistent_tournament_returns_404(client: TestClient) -> None:
    """Test GET /tournaments/nonexistent returns 404."""
    r = client.get("/tournaments/nonexistent-xyz")
    assert r.status_code == 404


def test_post_tournaments_with_zero_battles_returns_422(client: TestClient) -> None:
    """Test POST /tournaments with battles=0 returns 422."""
    r = client.post("/tournaments", json={"battles": 0})
    assert r.status_code == 422


def test_get_report_when_not_completed_returns_425(client: TestClient) -> None:
    """Test GET /tournaments/{job_id}/report when not completed returns 425."""
    import threading
    from jobs.jobs import BackgroundWorker

    # Create a slow-running job using BackgroundWorker
    from api.dependencies import get_job_repo
    repo = InMemoryJobRepository()
    worker = BackgroundWorker(repo)
    app.dependency_overrides[get_job_repo] = lambda: repo
    app.dependency_overrides[get_worker] = lambda: worker

    _slow_started = threading.Event()
    _slow_done = threading.Event()

    def _slow_fn() -> dict:
        _slow_started.set()
        _slow_done.wait(timeout=5)
        return {"total_battles": 1, "hero_wins": 1, "monster_wins": 0}

    repo.create("slow-job")
    worker.submit("slow-job", _slow_fn)
    _slow_started.wait(timeout=2)

    # Now try to get report while job is running
    client_test = TestClient(app, raise_server_exceptions=False)
    r = client_test.get("/tournaments/slow-job/report")
    _slow_done.set()
    assert r.status_code == 425
