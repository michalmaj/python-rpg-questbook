from fastapi import FastAPI
from api.routers import tournaments

app = FastAPI(
    title="Concurrent Tournament Runner",
    version="7.0",
    description="Non-blocking tournament API with job tracking.",
)
app.include_router(tournaments.router, tags=["tournaments"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
