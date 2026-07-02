# Mission 05: Dependencies and Repositories

## Goal

Replace manual service construction inside routers with FastAPI's `Depends()`
system. Add session persistence endpoints powered by `SessionRepository`.

## Game Problem

`monsters.py` and `battles.py` both create a `BattleService` object at module
level:

```python
_service = BattleService(monster_repo=MonsterRepository(DATA_DIR / "monsters.json"))
```

This pattern has problems:

- Every router module that needs a service creates its own copy — wasted
  resources.
- Swapping the implementation (e.g. from JSON file to database) means editing
  every router.
- Writing tests is harder because you cannot inject a fake service without
  monkey-patching module globals.

FastAPI solves this with **dependency injection**: you define factory functions
once, declare them as `Depends()` in endpoint signatures, and FastAPI wires
everything together for you.

## Python Concept

**`Depends()` and dependency injection** let you declare what a function needs
without constructing it yourself:

```python
from fastapi import Depends

def get_monster_repo() -> MonsterRepository:
    return MonsterRepository(DATA_DIR / "monsters.json")

def get_battle_service(
    repo: MonsterRepository = Depends(get_monster_repo),
) -> BattleService:
    return BattleService(monster_repo=repo)

@router.get("/monsters")
def list_monsters(
    service: BattleService = Depends(get_battle_service),
) -> list[MonsterOut]:
    return [MonsterOut(**vars(m)) for m in service.get_available_monsters()]
```

FastAPI reads the type annotation, sees `Depends(get_battle_service)`, calls
that function (which in turn calls `Depends(get_monster_repo)`), and passes the
result as the `service` argument — all before your route function runs.

### Minimal Example

```python
# task/dependencies.py
from fastapi import Depends

def get_db_connection() -> str:
    return "sqlite:///game.db"

def get_hero_repo(db: str = Depends(get_db_connection)) -> dict:
    return {"db": db, "table": "heroes"}

# task/routers/heroes.py
from fastapi import APIRouter, Depends
from task.dependencies import get_hero_repo

router = APIRouter()

@router.get("/heroes")
def list_heroes(repo: dict = Depends(get_hero_repo)) -> dict:
    return repo
```

## Add It to the Game

This mission's scaffold already has working `/monsters` and `/battle/simulate`
endpoints — but they use the "smelly" module-level `_service`. Your job is to
wire `Depends()` through everything and add session endpoints.

**Step 1 — Create `task/dependencies.py`**

```python
from fastapi import Depends
from task.config import DATA_DIR
from task.rpg.repositories import MonsterRepository, SessionRepository
from task.rpg.services import BattleService


def get_monster_repo() -> MonsterRepository:
    return MonsterRepository(DATA_DIR / "monsters.json")


def get_session_repo() -> SessionRepository:
    return SessionRepository(DATA_DIR / "sessions")


def get_battle_service(
    repo: MonsterRepository = Depends(get_monster_repo),
) -> BattleService:
    return BattleService(monster_repo=repo)
```

**Step 2 — Refactor `task/routers/monsters.py`**

Remove the module-level `_service` variable. Import `get_battle_service` from
`task.dependencies` and add it as a `Depends()` parameter:

```python
from fastapi import APIRouter, Depends
from task.dependencies import get_battle_service
from task.rpg.services import BattleService

router = APIRouter()

@router.get("/monsters", response_model=list[MonsterOut])
def list_monsters(
    service: BattleService = Depends(get_battle_service),
) -> list[MonsterOut]:
    return [MonsterOut(**vars(m)) for m in service.get_available_monsters()]
```

**Step 3 — Refactor `task/routers/battles.py`**

Same pattern: remove `_service`, inject via `Depends(get_battle_service)`:

```python
@router.post("/battle/simulate", response_model=BattleResultOut)
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

**Step 4 — Implement `task/routers/sessions.py`**

Add `POST /sessions` and `GET /sessions/{session_id}`. Both inject their
dependencies via `Depends()`:

```python
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from task.dependencies import get_battle_service, get_session_repo
from task.rpg.domain import HeroClass
from task.rpg.repositories import SessionRepository
from task.rpg.services import BattleService, create_hero

router = APIRouter()


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


@router.post("/sessions", status_code=201)
def create_session(
    req: BattleRequest,
    service: BattleService = Depends(get_battle_service),
    session_repo: SessionRepository = Depends(get_session_repo),
) -> dict:
    hero = create_hero(req.hero_name, req.hero_class)
    try:
        result = service.simulate(hero, req.monster_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    session_id = str(uuid.uuid4())
    session_repo.save(session_id, result)
    return {"session_id": session_id}


@router.get("/sessions/{session_id}", response_model=BattleResultOut)
def get_session(
    session_id: str,
    session_repo: SessionRepository = Depends(get_session_repo),
) -> BattleResultOut:
    result = session_repo.get(session_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    return BattleResultOut(**vars(result))
```

## Try It Yourself

1. Start the server: `uv run uvicorn task.main:app --reload`
2. Open <http://127.0.0.1:8000/docs>
3. Try `GET /monsters` — confirm it still returns the monster list.
4. Try `POST /sessions` with:
   ```json
   {"hero_name": "Ada", "hero_class": "rogue", "monster_name": "Orc"}
   ```
5. Copy the `session_id` from the response and call
   `GET /sessions/{session_id}` — confirm you get the battle result back.
6. Call `GET /sessions/fake-id` — confirm you get a `404`.

## Break It

- Remove `Depends(get_battle_service)` from a route function and just call
  `BattleService(...)` directly inside the function body. Run `check.py`. It
  should still pass functionally — but now study what the refactor buys you:
  if you later change `get_battle_service` to inject a mock, the direct
  instantiation won't benefit.
- Delete `task/dependencies.py` and run `check.py`. You should see:
  `❌ task/dependencies.py not found`.
- Add `Depends(get_session_repo)` to `list_monsters()`. FastAPI won't complain
  — but it is wasteful. `Depends()` only adds value when you actually use the
  injected object.

## Fix It

- Restore `task/dependencies.py`.
- Keep `Depends()` only where the dependency is used.
- Run `uv run python check.py` until it prints ✅.

## Side Quest

Modify `get_session_repo` in `dependencies.py` to accept a `sessions_dir: Path`
parameter with a default, so tests can override it:

```python
def get_session_repo(
    sessions_dir: Path = DATA_DIR / "sessions",
) -> SessionRepository:
    return SessionRepository(sessions_dir)
```

This is the pattern used in real FastAPI apps to make dependencies testable
without monkey-patching global state.

## Real-World Translation

| Game concept | Real world |
|---|---|
| `get_monster_repo()` | `get_db_session()` in SQLAlchemy apps |
| `get_battle_service(repo=Depends(...))` | Service that depends on a repository |
| `session_repo.save(session_id, result)` | Writing a record to a database |
| `Depends()` in route signature | Declaring what a handler needs, not how to get it |

Every production FastAPI project separates dependency wiring (`dependencies.py`)
from business logic (services) from HTTP handling (routers). Learning it here
sets you up to read and contribute to real codebases immediately.

## Checklist

- [ ] `task/dependencies.py` defines `get_monster_repo`, `get_session_repo`, and `get_battle_service`
- [ ] `Depends()` is used in at least one router file (not just in comments)
- [ ] `GET /monsters` returns 200 with a non-empty list
- [ ] `POST /battle/simulate` returns 200 with a `winner` field
- [ ] `POST /sessions` returns 201 with a `session_id` field
- [ ] `GET /sessions/{session_id}` returns 200 with a `winner` field
- [ ] `GET /sessions/nonexistent-id` returns 404
- [ ] `uv run python check.py` prints ✅ Mission 05 complete!
