# Project 01: Validated Bestiary

**Requires:** Level 3, Missions 01–03 (External Data Is Untrusted, Pydantic Monster Config, Load Game Catalogs)

## What you will build

A battle-hardened monster loader: it reads a JSON catalog, validates every record with Pydantic, and collects errors instead of crashing. A single bad monster never poisons the whole bestiary.

## What you must implement

| Requirement | Concept from |
|---|---|
| `MonsterModel(BaseModel)` — validates `hp > 0`, `gold ≥ 0`, `attack_type` in {"melee","ranged","magic"} | M02 |
| `MonsterDomain` — plain Python dataclass used inside the game | M03 |
| `to_domain(model)` — converts `MonsterModel` → `MonsterDomain` | M03 |
| `load_bestiary(path)` — returns `(valid_monsters, error_messages)`, never raises on bad records | M01, M03 |

## Structure

```
01_validated_bestiary/
├── README.md       ← this file
├── task.py         ← implement everything here
├── check.py        ← run to verify
└── data/
    └── monsters.json   ← sample file for manual exploration
```

## How to check

```bash
cd level_3_validation_and_persistence/projects/01_validated_bestiary
uv run python check.py
```

## load_bestiary contract

```python
valid, errors = load_bestiary(Path("data/monsters.json"))
```

- `valid` — list of `MonsterDomain` objects that passed validation
- `errors` — list of strings describing rejected records
- A single bad record must **not** prevent the rest from loading
- Error messages must be readable strings, not raw tracebacks

## Example

```python
# data/monsters.json contains 8 records: 4 valid, 4 invalid
valid, errors = load_bestiary(Path("data/monsters.json"))
print(f"Loaded {len(valid)} monsters, {len(errors)} errors")
for msg in errors:
    print(f"  ⚠ {msg}")
```

You can also test with your own JSON files — any list of objects works.

---

**Next:** [Project 02 — Save Slot Manager](../02_save_slot_manager/README.md)
