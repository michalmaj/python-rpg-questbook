# Project 02: Save Slot Manager

**Requires:** Level 3, Missions 01–05 (through Repository Pattern)

## What you will build

A save system with three slots backed by two interchangeable repositories: one that writes JSON files to disk, one that lives in memory. The game uses the same four-method interface regardless of which backend is active.

## What you must implement

| Requirement | Concept from |
|---|---|
| `SaveGameModel(BaseModel)` with `schema_version = 1` | M04 |
| `SaveRepository` Protocol: `save`, `load`, `list_slots`, `delete` | M05 |
| `JsonSaveRepository` — writes each slot as `slot_{n}.json` | M04, M05 |
| `InMemorySaveRepository` — dict-backed, no disk I/O | M05 |

## Structure

```
02_save_slot_manager/
├── README.md    ← this file
├── task.py      ← implement everything here
└── check.py     ← run to verify
```

## How to check

```bash
cd level_3_validation_and_persistence/projects/02_save_slot_manager
uv run python check.py
```

## Repository contract

Every repository must satisfy these four operations:

| Method | Description |
|---|---|
| `save(model)` | Persist the save for `model.slot` |
| `load(slot)` | Return `SaveGameModel` or `None` if slot is empty |
| `list_slots()` | Return sorted list of occupied slot numbers |
| `delete(slot)` | Remove the slot; no-op if already empty |

## Rules

- `load()` returns `None` for an empty slot — it must never raise `FileNotFoundError`
- `delete()` on an empty slot is a no-op — no exception
- JSON files must preserve **all** fields, including `schema_version`
- Both repositories must satisfy exactly the same behavioral contract

## Example

```python
repo = JsonSaveRepository(Path("saves/"))
repo.save(SaveGameModel(slot=1, hero_name="Ada", hero_hp=120, level=5, gold=100))
hero = repo.load(1)
print(hero.hero_name)   # Ada
print(repo.list_slots()) # [1]
repo.delete(1)
print(repo.load(1))     # None
```

---

**Next:** [Project 03 — SQLite Repository Backend (Boss Fight)](../03_sqlite_repository_backend/README.md)
