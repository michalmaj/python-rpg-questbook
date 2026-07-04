"""Mission 03: Async API Endpoints.

Goal:  Convert endpoints to async def and understand when it helps (I/O-bound)
       vs when it doesn't (CPU-bound like battle simulation).
Check: uv run python check.py (from mission folder)
"""
from fastapi import FastAPI
from task.routers import monsters, battles, tournaments

# TODO 1: Add description= to FastAPI() explaining async vs sync tradeoff
app = FastAPI(title="RPG Battle API")
app.include_router(monsters.router)
app.include_router(battles.router)
app.include_router(tournaments.router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
