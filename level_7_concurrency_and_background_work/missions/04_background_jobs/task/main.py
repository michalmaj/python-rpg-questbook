"""Mission 04: Background Jobs.

Goal:  Implement POST /tournaments → 202 + job_id and GET /jobs/{job_id}.
       Uses threading.Thread and a global _jobs dict (intentionally smelly).
Check: uv run python check.py (from mission folder)
"""
from fastapi import FastAPI
from task.routers import tournaments

app = FastAPI(title="RPG Background Jobs", version="4.0")
app.include_router(tournaments.router, tags=["tournaments"])


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
