# level_6_api/missions/07_api_tests/task/main.py
"""Mission 07: API Tests with TestClient.

Goal:  Write pytest tests for the RPG Battle API using FastAPI's TestClient
       and app.dependency_overrides for clean test isolation.
Check: uv run python check.py (from mission folder)
"""
from fastapi import FastAPI

from task.routers import battles, heroes, monsters, sessions

app = FastAPI(title="RPG Battle API", version="1.0")
app.include_router(monsters.router)
app.include_router(battles.router)
app.include_router(sessions.router)
app.include_router(heroes.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
