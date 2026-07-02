# Mission 04: API Routers

## Goal

Split endpoint functions into separate `APIRouter` modules and mount them on a
central `FastAPI` app in `task/main.py`.

## Game Problem

Your single-file API works — but as the RPG grows, one file will hold dozens of
endpoints: listing monsters, running battles, managing heroes, tracking gold.
Reading that file becomes painful, and merging changes from multiple developers
causes constant conflicts.

Real APIs split endpoints by domain. Monster endpoints live in
`routers/monsters.py`. Battle endpoints live in `routers/battles.py`. Each file
defines a standalone `APIRouter`. `main.py` just mounts them with
`app.include_router()`.

## Python Concept

**`APIRouter` and `include_router`** let you define route groups in separate
modules and assemble them in one place:

```python
# routers/monsters.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/monsters")
def list_monsters() -> list[dict]:
    ...
```

```python
# main.py
from fastapi import FastAPI
from task.routers import monsters

app = FastAPI()
app.include_router(monsters.router)
```

The `app` in `main.py` acts as the hub. Each router is a spoke that knows
nothing about the hub — it only knows its own endpoints.

### Minimal Example

```python
# task/routers/items.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/items")
def list_items() -> list[str]:
    return ["sword", "shield"]

@router.get("/items/{item_id}")
def get_item(item_id: int) -> dict:
    return {"id": item_id, "name": "sword"}
```

```python
# task/main.py
from fastapi import FastAPI
from task.routers import items

app = FastAPI()
app.include_router(items.router)
```

`GET /items` and `GET /items/{item_id}` are now registered on `app` even though
they are defined in a different file.

## Add It to the Game

This mission is a package: the `task/` folder is already a Python package with
`task/__init__.py` and `task/main.py`. Your job is to add the router layer.

**Step 1 — Create `task/routers/__init__.py`**

Create an empty file at `task/routers/__init__.py`. This turns `task/routers/`
into a package Python can import.

**Step 2 — Create `task/routers/monsters.py`**

```python
import dataclasses

from fastapi import APIRouter
from pydantic import BaseModel
from task.config import DATA_DIR
from task.rpg.repositories import MonsterRepository
from task.rpg.services import BattleService

router = APIRouter()

_service = BattleService(monster_repo=MonsterRepository(DATA_DIR / "monsters.json"))


class MonsterOut(BaseModel):
    name: str
    hp: int
    atk: int
    def_: int
    gold: int


@router.get("/monsters", response_model=list[MonsterOut])
def list_monsters() -> list[MonsterOut]:
    return [MonsterOut(**dataclasses.asdict(m)) for m in _service.get_available_monsters()]
```

Notice `DATA_DIR` comes from `task.config` — no hard-coded paths needed.

**Step 3 — Create `task/routers/battles.py`**

```python
import dataclasses

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from task.config import DATA_DIR
from task.rpg.domain import HeroClass
from task.rpg.repositories import MonsterRepository
from task.rpg.services import BattleService, create_hero

router = APIRouter()

_service = BattleService(monster_repo=MonsterRepository(DATA_DIR / "monsters.json"))


class BattleRequest(BaseModel):
    hero_name: str
    hero_class: HeroClass
    monster_name: str


class BattleResultOut(BaseModel):
    hero_name: str
    monster_name: str
    winner: str
    rounds: int
    gold_earned: int


@router.post("/battle/simulate", response_model=BattleResultOut)
def simulate_battle(req: BattleRequest) -> BattleResultOut:
    hero = create_hero(req.hero_name, req.hero_class)
    try:
        result = _service.simulate(hero, req.monster_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return BattleResultOut(**dataclasses.asdict(result))
```

**Step 4 — Mount the routers in `task/main.py`**

Add these lines after the `@app.get("/health")` block:

```python
from task.routers import monsters, battles

app.include_router(monsters.router)
app.include_router(battles.router)
```

Uncomment the four lines already shown as TODOs in `task/main.py`.

## Try It Yourself

1. Start the server: `uv run uvicorn task.main:app --reload`
2. Open <http://127.0.0.1:8000/docs>
3. Try `GET /monsters` — you should see Goblin, Orc, and Dragon.
4. Try `POST /battle/simulate` with:
   ```json
   {"hero_name": "Ada", "hero_class": "rogue", "monster_name": "Orc"}
   ```
5. Try adding a `GET /hero-classes` endpoint in `task/routers/battles.py` as a
   side quest.

## Break It

- Remove `app.include_router(monsters.router)` from `main.py` and call
  `GET /monsters`. What status code do you get? (`404` — the route was never
  registered.)
- Comment out `from fastapi import APIRouter` in `routers/monsters.py`. Run
  `check.py`. What error do you see?
- Try importing `DATA_DIR` incorrectly as `from config import DATA_DIR` (without
  the `task.` prefix). Run the server and observe the `ModuleNotFoundError`.

## Fix It

- Restore `app.include_router()` calls in `main.py`.
- Keep all imports as `from task.config import DATA_DIR` and
  `from task.rpg.xxx import ...` — the `task.` prefix is required when running
  uvicorn with the package form `task.main:app`.
- Run `uv run python check.py` until it prints ✅.

## Side Quest

Add a `GET /hero-classes` endpoint to `task/routers/battles.py`:

```python
@router.get("/hero-classes")
def list_hero_classes() -> list[str]:
    return _service.get_hero_classes()
```

Then visit <http://127.0.0.1:8000/docs> and confirm it appears in the docs.

## Real-World Translation

| Game concept | Real world |
|---|---|
| `routers/monsters.py` | `routers/products.py` in a shop API |
| `routers/battles.py` | `routers/orders.py` |
| `app.include_router(monsters.router)` | Mounting a blueprint (Flask) or sub-application |
| `task.config.DATA_DIR` | `settings.DATABASE_URL` in a config module |

Every FastAPI, Flask, and Django project uses this pattern. Learning it here —
with two small files — makes it easy to recognise and apply at scale.

## Checklist

- [ ] `task/routers/__init__.py` exists (empty file)
- [ ] `task/routers/monsters.py` defines `router = APIRouter()` and `GET /monsters`
- [ ] `task/routers/battles.py` defines `router = APIRouter()` and `POST /battle/simulate`
- [ ] `task/main.py` calls `app.include_router()` at least twice
- [ ] `GET /health` still returns 200
- [ ] `GET /monsters` returns 200 with a non-empty list
- [ ] `POST /battle/simulate` returns 200 with a `winner` field
- [ ] `uv run python check.py` prints ✅ Mission 04 complete!
