# Starter: Service-Ready RPG

**Prerequisite for Level 6 missions.**

A working RPG battle engine with domain, repositories, and a service layer.
Level 6 builds an HTTP API on top — you never touch these files during missions.

## Run the demo

```bash
cd starter_service_ready_rpg
uv run python main.py
```

## What's inside

| File | What it does |
|------|-------------|
| `rpg/domain.py` | `Hero`, `Monster`, `BattleResult`, `HeroClass` |
| `rpg/repositories.py` | `MonsterRepository` (JSON), `SessionRepository` (JSON per-file) |
| `rpg/services.py` | `BattleService`, `create_hero()`, `HERO_CLASS_STATS` |

## Tests

```bash
cd starter_service_ready_rpg
uv run pytest tests/ -q
```

All 10 tests should pass before you start Mission 01.
