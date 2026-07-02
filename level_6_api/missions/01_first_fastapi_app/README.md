# Mission 01: First FastAPI App

## Goal

Create a FastAPI app with two endpoints and see the automatic `/docs` page.

## Game Problem

The RPG battle engine works — but only on the command line. To share it with
other developers, mobile apps, or web frontends, we need to expose it over HTTP.
FastAPI turns Python functions into HTTP endpoints in a few lines.

## Python Concept — FastAPI basics

```python
from fastapi import FastAPI

app = FastAPI(title="My API")

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
```

Run it: `uvicorn task:app --reload`
Docs at: `http://127.0.0.1:8000/docs`

## Add to the Game

1. Import `FastAPI` and create `app = FastAPI(title="RPG Battle API", version="1.0")`
2. Add `GET /health` — returns `{"status": "ok"}`
3. Add `GET /monsters` — use the pre-wired `_service.get_available_monsters()`,
   return a `list[str]` of monster names
4. Run `uv run uvicorn task:app --reload` and visit `/docs`
5. Run `uv run python check.py` to confirm

## Try It Yourself

- Open `/docs` — click "Try it out" on GET /monsters and run it
- Add a `GET /` route that returns `{"message": "Welcome to the RPG API"}`
- What happens if you visit a path that doesn't exist?

## Checklist

- [ ] `app = FastAPI(...)` defined in `task.py`
- [ ] `GET /health` returns `{"status": "ok"}`
- [ ] `GET /monsters` returns a non-empty list
- [ ] `uv run python check.py` prints "Mission 01 complete!"
