"""Mission 08: Testing Background Work.

Goal:  Write tests for the background job system using SyncWorker.
       SyncWorker runs jobs inline — no threads, no race conditions.
Check: uv run python check.py (from mission folder)
"""
from fastapi import FastAPI
from task.routers import tournaments

app = FastAPI(title="RPG Job Repository", version="8.0")
app.include_router(tournaments.router, tags=["tournaments"])


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
