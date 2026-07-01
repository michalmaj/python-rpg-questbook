# Level 4: Interfaces and Reports

**Prerequisite:** Level 3 complete

## Goal

Your RPG now has domain logic, Pydantic validation, and a save/load system.
But how do users actually run it? How do you know what went wrong when something fails overnight?

Level 4 answers those questions by building a proper interface layer:

- CLI commands instead of hard-coded interactive prompts
- Structured logging instead of scattered `print()` calls
- Rich terminal output that makes information readable at a glance
- Session reports in JSON and Markdown — one for machines, one for humans
- A real entry point that installs `rpg` as a command you can run from anywhere

## The starting point

`starter_verbose_rpg/` is the output of Level 3 — a working, Pydantic-hardened RPG.
Open it and read the comments at the top. Six "interface smells" are labeled there.
Level 4 fixes them one mission at a time.

## Missions

| # | Folder | What you build |
|---|--------|----------------|
| 01 | `missions/01_argparse_baseline/` | CLI with `argparse` subcommands — stdlib baseline |
| 02 | `missions/02_typer_cli/` | Same commands rewritten with Typer — type hints as CLI contract |
| 03 | `missions/03_stdlib_logging/` | Replace `print()` technical output with `logging` |
| 04 | `missions/04_log_files/` | Route logs to `app.log` and `combat.log` with `FileHandler` |
| 05 | `missions/05_rich_terminal_output/` | Hero stats as a Rich `Table`, errors as a Rich `Panel` |
| 06 | `missions/06_session_reports/` | Pydantic report model → `session_*.json` + `session_*.md` |

## Boss Fight

`projects/01_installable_cli_tool/` — wire all six missions into one package and
register it as a real CLI entry point so `uv run rpg --help` works.

## How to start

```bash
# Read the starter's interface problems
open level_4_interfaces/starter_verbose_rpg/main.py

# Start Mission 01
open level_4_interfaces/missions/01_argparse_baseline/README.md
```

Track progress:

```bash
uv run python tools/course_status.py
```
