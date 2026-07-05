"""Mission 05: Job Status Repository.

Goal:  Refactor the global _jobs dict into a proper JobRepository.
       Use BackgroundWorker for local/single-process use, SyncWorker in tests.
Check: uv run python check.py (from mission folder)
"""
from fastapi import FastAPI
from task.routers import tournaments

app = FastAPI(title="RPG Job Repository", version="5.0")
app.include_router(tournaments.router, tags=["tournaments"])


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
