"""FastAPI application — wire the router here."""

from __future__ import annotations

from fastapi import FastAPI

from task.routers.monsters import router as monsters_router

app = FastAPI(title="Monster Catalog API")

app.include_router(monsters_router)
