# level_6_api/missions/08_openapi_and_api_polish/task/main.py
"""Mission 08: OpenAPI and API Polish.

Goal:  Give the RPG Battle API a proper identity — add metadata to FastAPI(),
       tag routers so /docs is easy to navigate, and annotate key endpoints.
Check: uv run python check.py (from mission folder)

Open README.md for step-by-step instructions.
"""
from fastapi import FastAPI

from task.routers import battles, heroes, monsters, sessions

# TODO 1: Add title, description, and version arguments to FastAPI().
# Open README.md for the exact values to use.
app = FastAPI()

# TODO 2: Add tags to each include_router() call.
# Open README.md for examples.
app.include_router(monsters.router)
app.include_router(battles.router)
app.include_router(sessions.router)
app.include_router(heroes.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
