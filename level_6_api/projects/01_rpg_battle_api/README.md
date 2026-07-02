# Boss Fight: RPG Battle API

You have learned all the FastAPI building blocks across Missions 01–08. Now wire them together into a complete, production-shaped battle API.

## What you are building

A 7-endpoint HTTP API backed by a JSON session store. The domain layer (domain, repositories, services) is pre-written. You implement the entire HTTP layer.

## What to implement

### 1. `rpg/api/schemas.py` — Pydantic API schemas

| Schema | Fields |
|--------|--------|
| `MonsterOut` | `name`, `hp`, `atk`, `def_`, `gold` |
| `BattleRequest` | `hero_name`, `hero_class` (HeroClass enum), `monster_name` |
| `BattleResultOut` | `hero_name`, `monster_name`, `winner`, `rounds`, `gold_earned` |
| `SessionCreated` | `session_id` |

### 2. `rpg/api/dependencies.py` — DI factories

```python
def get_monster_repo() -> MonsterRepository: ...
def get_session_repo() -> SessionRepository: ...
def get_battle_service(repo = Depends(get_monster_repo)) -> BattleService: ...
```

Use `Path(__file__).parents[2] / "data"` as the data directory.

### 3. `rpg/api/main.py` — FastAPI app

Create the `app = FastAPI(...)` instance and include all five routers.

### 4. `rpg/api/routers/` — Five routers

| File | Endpoint | Notes |
|------|----------|-------|
| `health.py` | `GET /health` | Returns `{"status": "ok", "version": "1.0"}` |
| `monsters.py` | `GET /monsters` | List all monsters |
| `heroes.py` | `GET /heroes/classes` | List hero class names |
| `battles.py` | `POST /battle/simulate` | Simulate battle; 404 if monster not found |
| `sessions.py` | `POST /sessions` (201) | Simulate + persist; return `{"session_id": "..."}` |
| `sessions.py` | `GET /sessions/{id}` | Retrieve stored result; 404 if missing |
| `sessions.py` | `GET /reports/{id}` | Return Markdown report; 404 if missing |

### 5. `tests/test_api.py` — API tests

Implement the 8 test stubs. Use only `TestClient` and `app.dependency_overrides` — no `unittest.mock`.

## DI pattern

Every endpoint that needs a service or repository must use `Depends()`:

```python
@router.post("/battle/simulate", response_model=BattleResultOut)
def simulate_battle(
    req: BattleRequest,
    service: BattleService = Depends(get_battle_service),
):
    ...
```

Never instantiate repositories or services manually inside a route function.

## check.py gates

Run the checker to see your progress:

```bash
uv run python level_6_api/projects/01_rpg_battle_api/check.py
```

| Gate | Check |
|------|-------|
| 1 | `GET /health` → 200 |
| 2 | `GET /monsters` → 200, non-empty list |
| 3 | `GET /heroes/classes` → 200, non-empty list |
| 4 | `POST /battle/simulate` → 200, `winner` in body |
| 5 | `POST /sessions` → 201, `session_id` in body |
| 6 | `GET /sessions/{valid_id}` → 200 |
| 7 | `GET /sessions/nonexistent-id` → 404 |
| 8 | `GET /reports/{valid_id}` → 200, body contains `##` |
| 9 | `pytest tests/test_api.py` → all pass |

## Running tests manually

```bash
cd level_6_api/projects/01_rpg_battle_api
uv run pytest tests/test_api.py -v
```

## Where to start

1. Read `rpg/domain.py`, `rpg/repositories.py`, and `rpg/services.py` to understand the pre-built layer.
2. Fill in `rpg/api/schemas.py` with the five Pydantic models.
3. Fill in `rpg/api/dependencies.py` with the three factory functions.
4. Implement `rpg/api/routers/health.py` and run `check.py` — Gate 1 should pass.
5. Work through the remaining routers one at a time, running `check.py` after each.
6. Implement the tests in `tests/test_api.py` last (or alongside each router).

Good luck!
