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


# TODO: write at least 6 tests covering:
# 1. POST /tournaments → 202 + job_id
# 2. GET /tournaments/{job_id} → completed with result
# 3. GET /tournaments/{job_id}/report → Markdown text/plain
# 4. GET /tournaments/nonexistent → 404
# 5. POST /tournaments with battles=0 → 422
# 6. GET /tournaments/{job_id}/report when not completed → 425
#
# Tip for test 6: create a job manually and set it to running:
#   from jobs.jobs import InMemoryJobRepository, JobStatus
#   repo = InMemoryJobRepository()
#   app.dependency_overrides[get_job_repo] = lambda: repo
#   repo.create("my-job")
#   repo.set_status("my-job", JobStatus.running)
#   r = client.get("/tournaments/my-job/report")
def test_placeholder() -> None:
    raise NotImplementedError("Implement the tests above")
