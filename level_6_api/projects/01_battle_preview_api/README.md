# Project 01: Battle Preview API

**Requires:** Level 6, Missions 01–03 (First FastAPI App, Request/Response Schemas, Routes Call Services)

## What you will build

A three-endpoint FastAPI app in a **single file**. No `APIRouter`, no `Depends` — just routes calling logic directly.

| Endpoint | What it does |
|---|---|
| `GET /health` | Liveness check → `{"status": "ok"}` |
| `POST /heroes/preview` | Validate hero data, return computed stats including `power_rating` |
| `POST /battle/simulate` | Look up monster, simulate combat, return winner and rounds |

## Structure

```
01_battle_preview_api/
├── README.md    ← this file
├── task.py      ← implement everything here
└── check.py     ← run to verify
```

## How to test

```bash
cd level_6_api/projects/01_battle_preview_api

# start the server
uv run uvicorn task:app --reload

# in another terminal — or use /docs in your browser
curl http://localhost:8000/health
curl -X POST http://localhost:8000/heroes/preview \
     -H "Content-Type: application/json" \
     -d '{"name":"Ada","hp":120,"atk":15,"def_":5}'

# run the automated checker (no server needed)
uv run python check.py
```

## Schemas

```python
# Input
HeroIn:      name, hp (>0), atk (>0), def_ (≥0)
BattleRequest: hero: HeroIn, monster_name: str

# Output
HeroPreview: name, hp, atk, def_, power_rating  # atk / (def_ + 1)
BattleResult: winner ("hero" | "monster"), rounds, hero_hp_remaining
```

## Rules

- `power_rating = round(hero.atk / (hero.def_ + 1), 2)`
- Each combat round: `damage = max(attacker.atk - defender.def_, 1)`
- Unknown `monster_name` → `HTTPException(status_code=404)`
- Invalid body (e.g. `hp=-1`) → 422 automatically (FastAPI/Pydantic)
- **No `APIRouter`** — that's Project 02. Keep this flat.

## Monster catalog

| Name | HP | ATK | DEF |
|---|---|---|---|
| Goblin | 30 | 8 | 2 |
| Orc | 60 | 12 | 4 |
| Dragon | 200 | 30 | 10 |

---

**Next:** [Project 02 — Monster Catalog API](../02_monster_catalog_api/README.md)
