# Project 02: Observable Battle Runner

**Requires:** Level 4, Missions 01–04 (through Log Files)

## What you will build

The Quest Master CLI, upgraded with structured logging. Every battle writes events to two log files so you can replay exactly what happened — without cluttering the terminal.

## What you must implement

| Requirement | Concept from |
|---|---|
| `setup_logging()` — configures `FileHandler` for `app.log` (INFO+) and `combat.log` (DEBUG+) | M03, M04 |
| `battle` command — runs the fight, logs each round to `combat.log`, result to `app.log` | M02, M04 |
| Unknown hero/monster → `typer.echo(err=True)` + `raise typer.Exit(1)`, error logged to `app.log` | M02 |

## Structure

```
02_observable_battle_runner/
├── README.md    ← this file
├── task.py      ← implement everything here
└── check.py     ← run to verify
```

## How to test

```bash
cd level_4_interfaces/projects/02_observable_battle_runner

# run a battle
uv run python task.py battle --hero Ada --monster Goblin

# inspect the logs
cat app.log
cat combat.log

# test error handling
uv run python task.py battle --hero Ada --monster Unknown

# run the checker
uv run python check.py
```

## Logging architecture

```
logging.getLogger("rpg")         → app.log     (INFO+)
logging.getLogger("rpg.combat")  → combat.log  (DEBUG+)
```

- `app.log`: battle start, result, errors
- `combat.log`: one line per combat round
- Terminal: only user-facing messages via `typer.echo()`
- **No `print()` for log output**

## Round logging example

```
# combat.log
2026-01-15 12:00:01 DEBUG rpg.combat Round 1: Ada deals 15 → Goblin HP 15/30
2026-01-15 12:00:01 DEBUG rpg.combat Round 2: Ada deals 15 → Goblin HP 0/30
2026-01-15 12:00:01 DEBUG rpg.combat Goblin defeated after 2 rounds
```

## Error handling

An unknown hero or monster must:
1. Print a friendly message: `typer.echo("Error: monster 'X' not found", err=True)`
2. Exit with code 1: `raise typer.Exit(1)`
3. Log the problem: `logger.error("Unknown monster: %s", name)`
4. **Never** let Python raise an unhandled exception to the terminal

---

**Next:** [Project 03 — Installable CLI Tool (Boss Fight)](../03_installable_cli_tool/README.md)
