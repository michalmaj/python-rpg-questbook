# Project 02: Monster Catalog API

**Requires:** Level 6, Missions 04–06 (API Routers, Dependencies and Repositories, API Errors and Status Codes)

## What you will build

A three-endpoint API split across a proper package structure. Uses `APIRouter`, `Depends()`, and `HTTPException(404)`.

| Endpoint | What it does |
|---|---|
| `GET /monsters` | List all monsters |
| `GET /monsters/{name}` | One monster by name, 404 if not found |
| `GET /monsters/{name}/difficulty` | `"easy"` / `"medium"` / `"hard"` rating |

## Structure

```
02_monster_catalog_api/
├── README.md
├── check.py
└── task/
    ├── __init__.py
    ├── main.py          ← FastAPI app, includes router (done)
    ├── schemas.py       ← MonsterOut, DifficultyOut (done)
    ├── dependencies.py  ← get_monster_repo() (done)
    ├── repository.py    ← Protocol + InMemoryMonsterRepository (implement this)
    └── routers/
        ├── __init__.py
        └── monsters.py  ← APIRouter with 3 endpoints (implement this)
```

Files marked **done** are pre-wired. You implement `repository.py` and `routers/monsters.py`.

## How to test

```bash
cd level_6_api/projects/02_monster_catalog_api

# start the server
uv run uvicorn task.main:app --reload

# test endpoints
curl http://localhost:8000/monsters
curl http://localhost:8000/monsters/Goblin
curl http://localhost:8000/monsters/Unknown
curl http://localhost:8000/monsters/Goblin/difficulty
curl http://localhost:8000/monsters/Dragon/difficulty

# run the automated checker (no server needed)
uv run python check.py
```

## Difficulty scale

| Difficulty | HP range |
|---|---|
| `easy` | HP ≤ 50 |
| `medium` | HP ≤ 150 |
| `hard` | HP > 150 |

## Key rules

- `InMemoryMonsterRepository.get_by_name()` must be **case-insensitive** (`"goblin"` == `"Goblin"`)
- Unknown monster → `HTTPException(status_code=404)`
- The router must use `Depends(get_monster_repo)` — no module-level dict in `monsters.py`
- `response_model=` declared on each endpoint (already in the scaffold)

## Dependency injection pattern

```python
@router.get("/{name}", response_model=MonsterOut)
def get_monster(name: str,
                repo: MonsterRepository = Depends(get_monster_repo)) -> MonsterOut:
    monster = repo.get_by_name(name)
    if monster is None:
        raise HTTPException(status_code=404, detail=f"Monster '{name}' not found")
    return monster
```

---

**Next:** [Project 03 — RPG Battle API (Boss Fight)](../03_rpg_battle_api/README.md)
