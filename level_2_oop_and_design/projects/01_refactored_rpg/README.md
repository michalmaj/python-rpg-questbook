# Project 01: Refactored RPG

**Requires:** Level 2, Missions 01–10

## What you will build

The same RPG that is in `starter_legacy_rpg/main.py`.

Only the code changes. The game feels identical to a player.

## What the refactored version must have

| Requirement | Concept from |
|---|---|
| `Hero` class with `__init__`, properties, methods | M01, M06 |
| `Monster` class with `take_damage()`, `is_alive` | M02, M06 |
| `Character` base class shared by both | M03 |
| Type hints on every function and method | M04 |
| `HeroClass` enum instead of `"warrior"` strings | M05 |
| `MonsterTemplate` dataclass for the monsters table | M07 |
| Code split across `hero.py`, `monster.py`, `combat.py`, `game.py` | M08 |
| `compute_damage()` as a pure function | M09 |
| At least 5 passing pytest tests | M10 |

## Structure

```
01_refactored_rpg/
├── README.md             ← this file
├── rpg/
│   ├── __init__.py
│   ├── hero.py
│   ├── monster.py
│   ├── combat.py
│   └── game.py           ← contains main(), run it to play
├── tests/
│   └── test_combat.py    ← at least 5 tests
└── check.py
```

## How to play

```bash
uv run python level_2_oop_and_design/projects/01_refactored_rpg/rpg/game.py
```

## How to test

```bash
uv run pytest level_2_oop_and_design/projects/01_refactored_rpg/tests/ -v
```

## Check

```bash
uv run python level_2_oop_and_design/projects/01_refactored_rpg/check.py
```

## Where to start

1. Start with `rpg/hero.py` — port the `Hero` class from Mission 01 + Mission 06
2. Then `rpg/monster.py` — port Monster + MonsterTemplate from Missions 02 + 07
3. Then `rpg/combat.py` — port pure functions from Mission 09 + add crit logic
4. Then `rpg/game.py` — port the main loop from the legacy `main.py`
5. Finally `tests/test_combat.py` — write tests for combat functions

You can reference the legacy code at any time:
```
level_2_oop_and_design/starter_legacy_rpg/main.py
```

But write the refactored version from scratch. Do not copy-paste the legacy code — translate it.

## Acceptance criteria

The check script verifies:
- All required files exist
- All 5+ tests pass
- `Hero`, `Monster`, `Character`, `HeroClass`, `MonsterTemplate` are importable from the `rpg` package
- `compute_damage` is a pure function (no prints, no global state)
- The `HeroClass` enum is used — not plain strings

---

*You inherited messy code. You fixed it. That is the job.*
