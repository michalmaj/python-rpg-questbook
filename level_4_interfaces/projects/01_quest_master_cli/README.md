# Project 01: Quest Master CLI

**Requires:** Level 4, Missions 01–02 (argparse Baseline, Typer CLI)

## What you will build

A three-command Typer CLI for your RPG. All data is hardcoded — the focus is on CLI design: subcommands, type hints as contract, and friendly error handling.

## Commands

| Command | What it does |
|---|---|
| `quest hero --name <name>` | Print a hero's stats card |
| `quest monsters` | List all available monsters |
| `quest battle --hero <name> --monster <name>` | Simulate a battle and print the result |

## Hardcoded data

You don't need to read files. Use these in your code:

**Heroes:** Ada (warrior, 120 HP), Zara (mage, 80 HP), Rex (ranger, 100 HP)

**Monsters:** Goblin (30 HP), Orc (60 HP), Dragon (200 HP)

## Structure

```
01_quest_master_cli/
├── README.md    ← this file
├── task.py      ← implement everything here
└── check.py     ← run to verify
```

## How to test

```bash
cd level_4_interfaces/projects/01_quest_master_cli

# test the CLI manually
uv run python task.py --help
uv run python task.py hero --name Ada
uv run python task.py monsters
uv run python task.py battle --hero Ada --monster Goblin
uv run python task.py battle --hero Unknown --monster Goblin

# run the automated checker
uv run python check.py
```

## Requirements

- `app = typer.Typer()` at module level
- Each command is an `@app.command()`
- Type hints on all parameters (Typer reads them)
- Unknown hero/monster name → friendly `typer.echo()` message + `raise typer.Exit(1)`
- **No raw Python traceback** should reach the terminal for bad input

## Example output

```
$ uv run python task.py hero --name Ada
Ada [WARRIOR]
HP: 120

$ uv run python task.py monsters
Goblin  HP: 30
Orc     HP: 60
Dragon  HP: 200

$ uv run python task.py battle --hero Ada --monster Goblin
Ada defeats Goblin after 4 rounds!

$ uv run python task.py battle --hero Unknown --monster Goblin
Error: hero 'Unknown' not found. Try: Ada, Zara, Rex
```

---

**Next:** [Project 02 — Observable Battle Runner](../02_observable_battle_runner/README.md)
