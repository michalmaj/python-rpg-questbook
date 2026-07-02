# level_6_api/missions/05_dependencies_and_repositories/task/main.py
"""Mission 05: Dependencies and Repositories.

Goal:  Replace manual service construction with FastAPI Depends().
       Add POST /sessions and GET /sessions/{session_id} using SessionRepository.
Check: uv run python check.py (from mission folder)
"""
from fastapi import FastAPI

from task.routers import battles, monsters, sessions

app = FastAPI(title="RPG Battle API", version="1.0")
app.include_router(monsters.router)
app.include_router(battles.router)
app.include_router(sessions.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
