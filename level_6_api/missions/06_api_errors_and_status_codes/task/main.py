# level_6_api/missions/06_api_errors_and_status_codes/task/main.py
"""Mission 06: API Errors and Status Codes.

Goal:  Replace bare exceptions with HTTPException and consistent status codes.
       Add an ErrorOut schema for structured error responses.
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
