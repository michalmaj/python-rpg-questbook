# Mission 06: API Errors and Status Codes

## Goal

Replace silent crashes and 500 errors with proper HTTP status codes and structured
error responses. Add `HTTPException` handling so clients always get a meaningful
status code and a consistent `{"detail": "..."}` body.

## Game Problem

The battle simulator currently crashes with a Python `ValueError` when a client
asks to fight an unknown monster:

```
POST /battle/simulate
{"hero_name": "Ada", "hero_class": "warrior", "monster_name": "FakeMonster"}
→ HTTP 500 Internal Server Error
```

A 500 tells the client "something went wrong on the server." But this isn't a
server bug — the client sent a bad monster name. The correct status is **404 Not
Found**, with a message explaining what was missing.

Similarly, `GET /heroes/classes` does not exist yet. A client that asks for
available hero classes gets a 404 from FastAPI itself, with no useful information.

## Python Concept

**`HTTPException`** is FastAPI's way of turning a Python exception into a proper
HTTP response. Raise it anywhere in a route function and FastAPI stops processing
and returns the response you specify:

```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Monster not found")
```

### Common status codes

| Code | Meaning | When to use |
|------|---------|-------------|
| 200 | OK | Successful GET, POST (default) |
| 201 | Created | Resource created (POST /sessions) |
| 400 | Bad Request | Client sent malformed data |
| 404 | Not Found | Resource does not exist |
| 422 | Unprocessable Entity | Pydantic validation failed (automatic) |
| 500 | Internal Server Error | Unhandled exception (never intentional) |

### `ErrorOut` schema

For consistent error responses across the API, define a Pydantic schema:

```python
# task/schemas.py
from pydantic import BaseModel

class ErrorOut(BaseModel):
    detail: str
```

You can use it as the `responses` annotation to document error shapes in the
OpenAPI spec:

```python
@router.post(
    "/battle/simulate",
    response_model=BattleResultOut,
    responses={404: {"model": ErrorOut}},
)
```

### Minimal Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

MONSTERS = {"Goblin": {"hp": 30}, "Orc": {"hp": 60}}


class ErrorOut(BaseModel):
    detail: str


@app.get("/monsters/{name}", responses={404: {"model": ErrorOut}})
def get_monster(name: str) -> dict:
    monster = MONSTERS.get(name)
    if monster is None:
        raise HTTPException(status_code=404, detail=f"Monster '{name}' not found")
    return monster
```

Try it:
- `GET /monsters/Goblin` → `{"hp": 30}` with status 200
- `GET /monsters/Dragon` → `{"detail": "Monster 'Dragon' not found"}` with status 404

## Add It to the Game

The scaffold has four tasks for you:

**Task 1 — Create `task/schemas.py`** with `ErrorOut`:

```python
# task/schemas.py
from pydantic import BaseModel


class ErrorOut(BaseModel):
    detail: str
```

**Task 2 — Fix `task/routers/battles.py`**

Import `HTTPException` and catch the `ValueError` from `service.simulate()`:

```python
from fastapi import APIRouter, Depends, HTTPException
from task.schemas import ErrorOut

@router.post(
    "/battle/simulate",
    response_model=BattleResultOut,
    responses={404: {"model": ErrorOut}},
)
def simulate_battle(
    req: BattleRequest,
    service: BattleService = Depends(get_battle_service),
) -> BattleResultOut:
    hero = create_hero(req.hero_name, req.hero_class)
    try:
        result = service.simulate(hero, req.monster_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return BattleResultOut(**vars(result))
```

**Task 3 — Implement `task/routers/heroes.py`**

Add the `GET /heroes/classes` endpoint:

```python
from fastapi import APIRouter, Depends
from task.dependencies import get_battle_service
from task.rpg.services import BattleService

router = APIRouter()


@router.get("/heroes/classes", response_model=list[str])
def list_hero_classes(
    service: BattleService = Depends(get_battle_service),
) -> list[str]:
    return service.get_hero_classes()
```

**Task 4 — Study `task/routers/sessions.py`**

The session endpoints already handle errors correctly. Read through
`create_session` and `get_session` to see the same `HTTPException` pattern applied
to POST and GET.

## Try It Yourself

1. Start the server: `uv run uvicorn task.main:app --reload`
2. Open <http://127.0.0.1:8000/docs>
3. Try `POST /battle/simulate` with `monster_name: "FakeMonster"` — confirm 404.
4. Try `POST /battle/simulate` with `monster_name: "Goblin"` — confirm 200.
5. Try `GET /heroes/classes` — confirm you see `["warrior", "mage", "rogue"]`.
6. Try `GET /sessions/fake-id-123` — confirm 404.
7. Open <http://127.0.0.1:8000/docs> and check the 404 response schema appears
   for `/battle/simulate` after you add `responses={404: {"model": ErrorOut}}`.

## Break It

- Remove the `try/except` in `simulate_battle` and call `check.py`. You should
  see `❌ Unknown monster should return 404, got 500`.
- Delete `task/schemas.py` and add `ErrorOut` inline in `battles.py`. Does the
  check still pass? (Yes — `check.py` only checks behaviour, not file location.)
- Change `status_code=404` to `status_code=400`. Run `check.py`. It fails because
  the check expects exactly 404.

## Fix It

- Restore the `try/except` and `status_code=404`.
- Run `uv run python check.py` until it prints ✅.

## Side Quest

Add a `GET /monsters/{name}` endpoint that returns a single monster or 404:

```python
@router.get(
    "/monsters/{name}",
    response_model=MonsterOut,
    responses={404: {"model": ErrorOut}},
)
def get_monster(
    name: str,
    service: BattleService = Depends(get_battle_service),
) -> MonsterOut:
    monster = service._repo.get(name)
    if monster is None:
        raise HTTPException(status_code=404, detail=f"Monster '{name}' not found")
    return MonsterOut(**vars(monster))
```

Notice `service._repo.get(name)` accesses the private attribute — that's a hint
that a cleaner design would expose `get_monster(name)` on `BattleService` itself.
Can you add that method?

## Real-World Translation

| Game concept | Real world |
|---|---|
| `HTTPException(status_code=404)` | Standard not-found response in every HTTP API |
| `ErrorOut(detail: str)` | Consistent error schema (matches FastAPI default) |
| `responses={404: {"model": ErrorOut}}` | OpenAPI documentation for error shapes |
| Catching `ValueError`, re-raising as `HTTPException` | Converting domain errors to HTTP errors at the boundary |

Catching domain exceptions at the HTTP layer and converting them to status codes
keeps your business logic clean. `BattleService.simulate` doesn't know anything
about HTTP — it just raises a `ValueError`. The router is the translation layer.

## Checklist

- [ ] `task/schemas.py` defines `ErrorOut` with a `detail: str` field
- [ ] `HTTPException` is imported and used in `task/routers/battles.py`
- [ ] `POST /battle/simulate` with an unknown monster returns 404 (not 500)
- [ ] `POST /battle/simulate` with a known monster returns 200
- [ ] `GET /sessions/nonexistent` returns 404
- [ ] `GET /heroes/classes` returns 200 with a non-empty list of class names
- [ ] `uv run python check.py` prints ✅ Mission 06 complete!
