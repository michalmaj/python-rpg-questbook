"""Background Report Queue — FastAPI application entry point.

Pre-implemented — do not modify this file.
Run with: uvicorn task.main:app --reload
"""

from fastapi import FastAPI

from task.routers.reports import router as reports_router

app = FastAPI(title="Background Report Queue")

app.include_router(reports_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
