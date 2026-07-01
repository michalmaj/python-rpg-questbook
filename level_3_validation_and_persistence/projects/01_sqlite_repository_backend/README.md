# Boss Fight: SQLite Repository Backend

## Goal

Add a second persistence backend — SQLite — using the same `SaveRepository` and `CombatLogRepository` protocols you defined in Missions 05 and 06. The game code changes in one place: the backend is swapped. Nothing else moves.

## You will learn

- Python's built-in `sqlite3` module
- `CREATE TABLE IF NOT EXISTS`, `INSERT OR REPLACE`, `SELECT`
- How a well-designed abstraction makes switching backends trivial
- Why "the game doesn't know which backend is running" is a sign of good design

## The payoff

After Mission 05 you have:

```python
class SaveRepository(Protocol):
    def save(self, hero: Hero) -> None: ...
    def load(self) -> Hero | None: ...
```

And two implementations:
- `JsonSaveRepository` — writes `save_game.json`
- `InMemorySaveRepository` — stores in a variable

Today you add a third:
- `SqliteSaveRepository` — reads and writes a `saves.db` SQLite database

The game loop passes in a `SaveRepository`. It calls `repo.save(hero)` and `repo.load()`. It does not know — and does not care — whether the backend is JSON or SQLite.

```python
# swap the backend here and nothing else changes:
repo: SaveRepository = SqliteSaveRepository(DB_PATH)
# repo: SaveRepository = JsonSaveRepository(SAVE_FILE)
```

## The same for combat logs

After Mission 06 you have `CombatLogRepository`. Today you add:
- `SqliteCombatLogRepository` — appends rows to a `combat_log` table

## What you need to build

```
projects/01_sqlite_repository_backend/
├── rpg/
│   ├── __init__.py
│   ├── domain.py        # Hero, HeroClass, CombatLogRow (from missions)
│   ├── save_repo.py     # SaveRepository Protocol + JsonSaveRepository + SqliteSaveRepository
│   └── log_repo.py      # CombatLogRepository Protocol + CsvCombatLogRepository + SqliteCombatLogRepository
├── task.py              # wire everything together, run a demo session
└── check.py             # verifies both SQLite implementations
```

The `rpg/domain.py`, `rpg/save_repo.py`, and `rpg/log_repo.py` files contain the finished code from missions 04–06 plus your new SQLite classes.

## sqlite3 primer

Python includes `sqlite3` in the standard library — no install needed.

```python
import sqlite3
from pathlib import Path

con = sqlite3.connect("saves.db")    # creates the file if it doesn't exist
cur = con.cursor()

# create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS saves (
        id          INTEGER PRIMARY KEY,
        schema_ver  INTEGER NOT NULL,
        hero_json   TEXT NOT NULL
    )
""")
con.commit()

# insert (or replace the single row — we only keep one save per game)
cur.execute("INSERT OR REPLACE INTO saves VALUES (1, ?, ?)", (1, '{"name": "Ada"}'))
con.commit()

# query
cur.execute("SELECT hero_json FROM saves WHERE id = 1")
row = cur.fetchone()
if row:
    print(row[0])   # '{"name": "Ada"}'

con.close()
```

## SqliteSaveRepository design

Store one row per save slot. For simplicity, always use `id = 1` (single save slot). Store the hero as JSON text — let `SaveGameModel` handle serialisation:

```
saves table:
  id         INTEGER PRIMARY KEY   (always 1 for single-slot)
  schema_ver INTEGER
  hero_json  TEXT                  (SaveGameModel.model_dump_json())
```

`save(hero)`:
1. Create a `SaveGameModel` from the hero
2. `INSERT OR REPLACE INTO saves VALUES (1, schema_version, json_text)`

`load() -> Hero | None`:
1. `SELECT schema_ver, hero_json FROM saves WHERE id = 1`
2. If no row → return `None`
3. Validate schema version → raise `ValueError` if mismatch
4. `SaveGameModel.model_validate_json(hero_json).to_hero()`

## SqliteCombatLogRepository design

Each combat turn is one row in `combat_log`:

```
combat_log table:
  id            INTEGER PRIMARY KEY AUTOINCREMENT
  battle_id     INTEGER
  turn          INTEGER
  hero_name     TEXT
  hero_class    TEXT
  monster       TEXT
  action        TEXT
  damage_dealt  INTEGER
  damage_taken  INTEGER
  hero_hp       INTEGER
  monster_hp    INTEGER
  result        TEXT
```

`append(row)`:
- `INSERT INTO combat_log (battle_id, turn, ...) VALUES (?, ?, ...)`

`read_all()`:
- `SELECT * FROM combat_log ORDER BY id`
- Convert each row to `CombatLogRow`

## Run

```bash
uv run python level_3_validation_and_persistence/projects/01_sqlite_repository_backend/task.py
```

## Check

```bash
uv run python level_3_validation_and_persistence/projects/01_sqlite_repository_backend/check.py
```

## Break it on purpose

Open `saves.db` with a SQLite viewer (or the `sqlite3` CLI) and change `schema_ver` to `99`. Run `load()`. You should get a `ValueError` — the same error as in Mission 04, just from a different backend.

## Fix it

Run `save(hero)` again to overwrite the row with the correct schema version.

## Side quest

Write a test that runs a session with `SqliteSaveRepository`, then switches to `JsonSaveRepository`, and verifies that the hero is gone (different backends, no shared state). This shows that the Protocol abstraction is genuinely backend-independent.

## Real-world translation

Django's ORM lets you swap `sqlite3` for PostgreSQL by changing one setting. Your `SaveRepository` Protocol is a hand-built version of the same idea. In production systems, this pattern is called the **Adapter** design pattern.

## Checklist

- [ ] `SqliteSaveRepository.save()` writes hero to SQLite
- [ ] `SqliteSaveRepository.load()` reads hero back; returns `None` if no row
- [ ] `SqliteSaveRepository.load()` raises `ValueError` on schema version mismatch
- [ ] `SqliteCombatLogRepository.append()` inserts a row into the `combat_log` table
- [ ] `SqliteCombatLogRepository.read_all()` returns all rows as `CombatLogRow` objects
- [ ] `task.py` can swap backends with a one-line change and the game logic is unchanged

---

Level 3 complete. You now have:

- Pydantic validation at every system boundary
- A versioned save format
- Two swappable persistence backends
- A validated, repository-isolated combat log
- Configuration in one place, overridable via environment variables
