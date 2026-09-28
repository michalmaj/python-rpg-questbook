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
projects/03_installable_cli_tool/
├── rpg/
│   ├── __init__.py
│   ├── domain.py       # Hero, Monster, HeroClass (pure domain, no changes)
│   ├── schemas.py      # SaveGameModel, SessionSummary (Pydantic boundary)
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

**Step 6: Understand the entry point — it's already registered in this repo.**

In a standalone project, this is the step where *you* add `[project.scripts]` to `pyproject.toml`. In this course, the repo-root `pyproject.toml` already has it — that one file is shared across every level in this monorepo, and `tools/author_check.py` relies on it too:

```toml
[project.scripts]
rpg = "rpg.cli:main"
```

Your job here isn't to add that line — it's to make what it points to actually work. `rpg.cli:main` means: import the `rpg.cli` module, call its `main()` function. `task.py` does the same wiring manually, so you can test without relying on the installed command at all:

```python
# task.py — run this manually to test all commands
from rpg.cli import app

if __name__ == "__main__":
    app()
```

`rpg/cli.py`'s own `main()` (at the bottom of the file) calls `app()` too — same object, reached two different ways. Once your `rpg/cli.py` is complete, `uv run rpg --help` runs *your* code, exactly like `uv run python task.py --help` does.

## Entry point mechanics

`[project.scripts]` tells Python's packaging system to create a wrapper script:

```toml
[project.scripts]
rpg = "rpg.cli:main"          # function to call
```

An editable/development install (`uv sync` here, or `pip install -e .` in a standalone project) makes the `rpg` package importable in this environment and wires up that wrapper. From that point on, `rpg` in the terminal calls `main()` in `rpg/cli.py` — regardless of which directory you are in — and `main()` just calls `app()`, the same Typer app your code defines.

This is how `pytest`, `ruff`, `typer`, and every other CLI tool you have used is installed.

## Package mental model

Four things are easy to blur together — worth separating:

- **A Python file/module** — one `.py` file, importable by its filename (`rpg/cli.py` is the module `rpg.cli`).
- **A package** — a directory with `__init__.py` (`rpg/`) that groups modules under one importable name.
- **A distribution/project** — the installable unit described by `pyproject.toml`: metadata, dependencies, and *which* packages it contains. This repo's `pyproject.toml` maps the deeply-nested `level_4_interfaces/projects/03_installable_cli_tool/rpg/` directory to the top-level importable name `rpg` (see `[tool.hatch.build.targets.wheel]`) — that's why your code imports as `from rpg.domain import ...`, not some longer path.
- **A console entry point** — a mapping from a terminal command name to one Python callable, registered under `[project.scripts]`. Running `rpg` does not mean "run the file called rpg" — there is no such file. It means: the environment looks up the `rpg` command, finds `rpg.cli:main`, imports `rpg.cli`, and calls `main()`.

### Editable install

This repo is installed with `uv sync`, which performs a development ("editable") install of the project described by the root `pyproject.toml`. In practice that means:

- the `rpg` package becomes importable anywhere in this environment,
- the code Python actually runs still lives in this working source tree — nothing gets copied elsewhere,
- so editing `rpg/cli.py` and running `uv run rpg --help` again picks up your change immediately, with no reinstall step in between.

The exact mechanism an editable install uses to point back at your source tree is a build-backend detail (this repo uses `uv` with `hatchling`) — you don't need to know it to use the result correctly: install once, keep editing, no reinstall in between.

### `python -m`, direct file execution, and this project's entry point

Three ways to run Python code — not interchangeable:

- **`python some/path/file.py`** — runs that exact file directly. This is what `task.py` does here: `uv run python level_4_interfaces/projects/03_installable_cli_tool/task.py --help`.
- **`python -m package.module`** — asks Python's *import system* to find `package.module` (via `sys.path` / whatever is installed in the environment), then runs it as a module, with `__name__ == "__main__"`. This project's `rpg/cli.py` supports it: `uv run python -m rpg.cli --help` works, because the file ends with `if __name__ == "__main__": main()`.
- **Console entry point (`rpg` command)** — also goes through the import system, but maps a fixed command name to one specific callable (`rpg.cli:main`) instead of you spelling out a module path.

One thing this package does **not** support: `python -m rpg` — running the *package* itself, rather than a module inside it. That needs an `rpg/__main__.py`, which this project doesn't have; only `rpg/cli.py` is directly runnable with `-m`. If you want that shortcut, a good place to try it is the side quest below — add `rpg/__main__.py` that imports and calls `cli.main()`.

## Run

```bash
# test without installing
uv run python level_4_interfaces/projects/03_installable_cli_tool/task.py --help

# the entry point is already registered — uv sync once, then:
uv run rpg --help
uv run rpg new-game --name Ada --class warrior
uv run rpg simulate --battles 5
uv run rpg status
uv run rpg report
```

## Check

```bash
uv run python level_4_interfaces/projects/03_installable_cli_tool/check.py
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
- [ ] `uv run rpg --help` works and lists all five commands (the `[project.scripts]` entry is already registered in this repo's `pyproject.toml` — your job is to make what it points to actually work)
- [ ] `logs/app.log` and `logs/combat.log` are written during a session

---

Level 4 complete. You now have:

- A CLI that humans can use from the terminal
- A Typer app with typed commands and automatic help
- Structured logging to console and files
- Rich terminal output that communicates information clearly
- Session reports in two formats for both humans and machines
- An installable entry point — `rpg` is a real command
