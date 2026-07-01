# Mission 06: Combat Log Repository

## Goal

Extract combat logging from the game loop into a repository, using a Pydantic model to validate each row on the way in.

## You will learn

- Using Pydantic's `Literal` type for exact string constraints
- Applying the repository pattern to append-only logs (not just save/load)
- Why coupling file format to game logic makes testing hard
- `csv.DictWriter` / `csv.DictReader` with Pydantic models

## Game problem

In the starter RPG, logging happens directly inside `run_combat()`:

```python
def _append_log_row(battle_id, turn, hero, monster, action, ...):
    with LOG_FILE.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([battle_id, turn, ...])
```

Problems:

1. `run_combat()` is coupled to the CSV file path and format — impossible to test without writing files.
2. There is no validation — any string can go into the `action` column; `damage_dealt` could be negative.
3. Changing the format (e.g., to JSON Lines) means touching the combat loop.

The fix: a `CombatLogRepository` that receives a typed `CombatLogRow` and handles storage.

## Python concept

**`Literal`** constrains a string field to a fixed set of allowed values:

```python
from typing import Literal
from pydantic import BaseModel

class CombatLogRow(BaseModel):
    action: Literal["attack", "potion"]   # only these two strings allowed
    result: Literal["ongoing", "win", "loss"]
```

**`csv.DictWriter`** writes dicts; `csv.DictReader` reads them back as dicts:

```python
import csv

# write:
with path.open("a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["battle_id", "turn", ...])
    writer.writerow(row.model_dump())

# read:
with path.open(newline="") as f:
    for raw in csv.DictReader(f):
        row = CombatLogRow.model_validate(raw)   # CSV values are strings — Pydantic coerces them
```

## Your task

Open `task.py`. `CombatLogRow` is already defined.

Implement:

1. **`CsvCombatLogRepository.append(row)`** — write the row to a CSV file; write the header only if the file does not exist yet
2. **`CsvCombatLogRepository.read_all()`** — return `[]` if no file; parse each CSV row into `CombatLogRow`
3. **`InMemoryCombatLogRepository.append(row)`** — add to `self._rows`
4. **`InMemoryCombatLogRepository.read_all()`** — return a copy of `self._rows`

## Run

> Before you complete the TODOs, running `task.py` will print a friendly reminder instead of crashing.

```bash
uv run python level_3_validation_and_persistence/missions/06_combat_log_repository/task.py
```

## Check

```bash
uv run python level_3_validation_and_persistence/missions/06_combat_log_repository/check.py
```

## Break it on purpose

Try creating a `CombatLogRow` with `action="run"` or `damage_dealt=-5`. Pydantic should raise a `ValidationError` before the row reaches the file.

## Fix it

Use only `action="attack"` or `action="potion"`, and keep `damage_dealt >= 0`. The constraints are enforced at the model level — the repository never sees invalid data.

## Side quest

Write a test that verifies a simulated combat sequence produces the correct number of log rows and that the final row has `result="win"` or `result="loss"`:

```python
def test_combat_logs_final_result():
    repo = InMemoryCombatLogRepository()
    # ... simulate rows ...
    rows = repo.read_all()
    assert rows[-1].result in ("win", "loss")
```

## Real-world translation

Event sourcing and audit logs use the same pattern: append-only, validated, format-agnostic. Apache Kafka, AWS Kinesis, and database write-ahead logs all follow the idea: you append immutable, validated records; you can replay them to reconstruct state.

## Checklist

- [ ] `CsvCombatLogRepository.append()` writes validated rows to CSV
- [ ] `CsvCombatLogRepository.read_all()` parses CSV rows back into `CombatLogRow`
- [ ] `InMemoryCombatLogRepository` works without touching any file
- [ ] I understand why `Literal["attack", "potion"]` is better than a raw `str`
- [ ] I can explain: why is combat logging in the repository instead of in `run_combat()`?

---

Next mission: `level_3_validation_and_persistence/missions/07_settings_and_paths/README.md`
