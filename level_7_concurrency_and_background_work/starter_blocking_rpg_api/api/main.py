from fastapi import FastAPI
from api.routers import monsters, battles, tournaments

app = FastAPI(
    title="RPG Battle API (Blocking)",
    version="7.0",
    description="Starter for Level 7 — simulate_tournament() blocks the request thread.",
)
app.include_router(monsters.router, tags=["monsters"])
app.include_router(battles.router, tags=["battles"])
app.include_router(tournaments.router, tags=["tournaments"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
