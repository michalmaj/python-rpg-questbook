# Boss Fight: Installable CLI Tool

## Goal

Wire everything from Missions 01–06 into one installable CLI tool. After completing this project, running:

```bash
rpg new-game --name Ada --class warrior
rpg simulate --battles 10
rpg play
rpg report
rpg status
```

...works from anywhere in the terminal — not just from the mission directory.

## You will learn

- `[project.scripts]` in `pyproject.toml` — the entry point that makes `rpg` a real command
- How to structure a CLI application as a Python package
- How all six interface concepts compose into one tool
- Why the domain layer stays unchanged — only the interface layer is new

## The payoff

After Missions 01–06 you have:

| Mission | Concept | What it adds |
|---------|---------|-------------|
| M01     | argparse | CLI args instead of input() |
| M02     | Typer    | Type-safe commands, auto-help |
| M03     | logging  | Technical events separated from user output |
| M04     | log files | Persistent logs, app.log + combat.log |
| M05     | Rich     | Readable tables, panels, stderr errors |
| M06     | Reports  | session_*.json + session_*.md on exit |

This project wires them all together. The game domain (Hero, Monster, combat logic) does not change — only the interface layer around it.

## What you need to build

```
projects/01_installable_cli_tool/
├── rpg/
│   ├── __init__.py
│   ├── domain.py       # Hero, Monster, HeroClass (pure domain, no changes)
│   ├── schemas.py      # SaveGameModel, SessionSummary (Pydantic boundary)
│   ├── settings.py     # GameSettings via pydantic-settings
│   ├── game.py         # Core game logic: load_monsters, run_combat, simulate
│   ├── output.py       # Rich output: show_hero_stats, show_combat_result, ...
│   ├── logging_setup.py # setup_logging, add_file_handler, setup_log_files
│   └── cli.py          # Typer app: new-game, play, simulate, report, status
├── data/               # monsters.json, hero_classes.json, weapons.json
├── task.py             # wire everything; run manually to test
└── check.py            # verifies the installable entry point
```

## Steps — read before you start

**Step 1: Port domain + schemas from M06.**
`rpg/domain.py` contains `Hero`, `HeroClass`, `Monster` as pure dataclasses.
`rpg/schemas.py` contains `SaveGameModel` and `SessionSummary`.
Neither file imports from the other; neither imports Typer or Rich.

**Step 2: Port `output.py` from M05.**
Copy `show_hero_stats`, `show_combat_start`, `show_combat_result`, `show_error` from M05.
These are the same four functions — just moved into the package.

**Step 3: Port `logging_setup.py` from M03 + M04.**
Combine `setup_logging`, `add_file_handler`, `setup_log_files` into one module.

**Step 4: Port game logic into `game.py`.**
Move `load_monsters`, `save_game`, `load_game`, `run_combat`, `simulate_battles`
from the starter. These functions are unchanged — they use domain objects and call
the output functions via dependency injection (pass `console` or use `output.py`).

**Step 5: Build the CLI in `cli.py`.**
Create the Typer app with five commands:
- `new-game --name NAME --class CLASS` — create and save a hero
- `play` — interactive game loop
- `simulate --battles N` — auto-simulate N battles
- `report` — show the most recent session report
- `status` — show current save

**Step 6: Register the entry point.**
In `task.py`:

```python
# task.py — run this manually to test all commands
from rpg.cli import app

if __name__ == "__main__":
    app()
```

And in `pyproject.toml` (the repo root):

```toml
[project.scripts]
rpg = "level_4_interfaces.projects.01_installable_cli_tool.rpg.cli:app"
```

After `uv sync`, `rpg` is available as a command.

## Entry point mechanics

`[project.scripts]` tells Python's packaging system to create a wrapper script:

```toml
[project.scripts]
rpg = "rpg.cli:app"          # function to call
```

`uv sync` (or `pip install -e .`) installs the script. From that point on, `rpg` in the terminal calls `app()` in `rpg/cli.py` — regardless of which directory you are in.

This is how `pytest`, `ruff`, `typer`, and every other CLI tool you have used is installed.

## Run

```bash
# test without installing
uv run python level_4_interfaces/projects/01_installable_cli_tool/task.py --help

# after registering in pyproject.toml and running uv sync:
uv run rpg --help
uv run rpg new-game --name Ada --class warrior
uv run rpg simulate --battles 5
uv run rpg status
uv run rpg report
```

## Check

```bash
uv run python level_4_interfaces/projects/01_installable_cli_tool/check.py
```

## Break it on purpose

Remove `[project.scripts]` from `pyproject.toml`. Run `uv sync`. Run `rpg --help`.

```
error: No such command 'rpg'
```

The entry point is gone. The code still works via `python task.py`, but `rpg` no longer exists as a command.

## Fix it

Add `[project.scripts]` back, run `uv sync`. `rpg` is a command again.

## Side quest

Add `rpg clean` — a command that deletes all files in `saves/`, `logs/`, and `reports/` and confirms with `Are you sure? [y/N]` using `typer.confirm()`.

## Real-world translation

Every Python CLI tool you have installed — `pytest`, `ruff`, `black`, `httpie`, `fastapi-cli` — uses `[project.scripts]` (or the older `[console_scripts]` in `setup.cfg`). The pattern is always the same: a function in a module becomes a terminal command after installation.

## Checklist

- [ ] `rpg/domain.py` contains only pure dataclasses and enums (no Pydantic, no Typer, no Rich)
- [ ] `rpg/schemas.py` contains `SaveGameModel` and `SessionSummary`
- [ ] `rpg/cli.py` has a `typer.Typer()` app with five commands
- [ ] `new-game`, `simulate`, `status` work without interactive prompts
- [ ] `play` starts the interactive game loop
- [ ] `report` prints or opens the most recent session report
- [ ] A session report (`reports/session_*.json` and `.md`) is generated after `play` or `simulate`
- [ ] `[project.scripts]` is registered in `pyproject.toml` and `uv run rpg --help` works
- [ ] `logs/app.log` and `logs/combat.log` are written during a session

---

Level 4 complete. You now have:

- A CLI that humans can use from the terminal
- A Typer app with typed commands and automatic help
- Structured logging to console and files
- Rich terminal output that communicates information clearly
- Session reports in two formats for both humans and machines
- An installable entry point — `rpg` is a real command
