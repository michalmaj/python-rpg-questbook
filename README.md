# Python RPG Questbook

[![CI](https://github.com/michalmaj/python-rpg-questbook/actions/workflows/ci.yml/badge.svg)](https://github.com/michalmaj/python-rpg-questbook/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)

Learn Python by building a real terminal RPG — one mechanic at a time.

## What is this?

This is a Python course built around one growing story: you are building a terminal RPG game.

Each mission teaches one Python concept by adding a new game mechanic:

- variables store hero stats
- conditions decide who wins a battle
- loops run the combat
- files save the combat log
- data analysis asks: is the game balanced?

The course continues into professional Python territory — OOP, validation, persistence, APIs, and concurrency — using the same RPG as the vehicle.

## Setup

You need [uv](https://docs.astral.sh/uv/) installed. If you completed the setup course, you already have it.

```bash
git clone https://github.com/michalmaj/python-rpg-questbook.git
cd python-rpg-questbook
uv sync
```

## How to use this course

Open `COURSE_MAP.md` to see the full list of missions, then track your progress:

```bash
uv run python tools/course_status.py
```

For each mission, the workflow is the same:

```bash
# 1. Read the mission instructions
#    Open: level_1_python_basics/missions/01_hero_stats/README.md

# 2. Edit the task file
#    Open: level_1_python_basics/missions/01_hero_stats/task.py

# 3. Run your code
uv run python level_1_python_basics/missions/01_hero_stats/task.py

# 4. Check your solution
uv run python level_1_python_basics/missions/01_hero_stats/check.py
```

## Course structure

Seven levels, each with focused missions and two checkpoint projects before the boss fight:

```
level_1_python_basics/              ← Python fundamentals through terminal RPG + data analysis
  missions/                         ← 20 focused exercises (one concept each)
  projects/                         ← 5 boss fights that combine what you learned

level_2_oop_and_design/             ← OOP, refactoring, design patterns
  starter_legacy_rpg/               ← the code you will clean up
  missions/                         ← 10 missions
  projects/                         ← P01 Arena Roster · P02 Character Sheet Builder · P03 boss fight

level_3_validation_and_persistence/ ← Pydantic, repository pattern, SQLite
  starter_raw_rpg/                  ← the code you will harden
  missions/                         ← 7 missions
  projects/                         ← P01 Validated Bestiary · P02 Save Slot Manager · P03 boss fight

level_4_interfaces/                 ← CLI (Typer), logging, Rich output, reports, entry points
  starter_verbose_rpg/              ← the interface-smelly app you will improve
  missions/                         ← 6 missions
  projects/                         ← P01 Quest Master CLI · P02 Observable Battle Runner · P03 boss fight

level_5_maintainability/            ← ruff, mypy, pyright, pytest-cov, pre-commit, CI
  starter_unqualified_rpg/          ← working RPG with 6 quality smells (your starting point)
  missions/                         ← 9 missions
  projects/                         ← P01 Quality Gate Rescue · P02 Combat Regression Suite · P03 boss fight

level_6_api/                        ← FastAPI, schemas, routers, dependency injection, TestClient
  starter_service_ready_rpg/        ← working RPG engine with service layer (your API will call this)
  missions/                         ← 8 missions
  projects/                         ← P01 Battle Preview API · P02 Monster Catalog API · P03 boss fight

level_7_concurrency_and_background_work/  ← asyncio, job_id, ThreadPoolExecutor, ProcessPoolExecutor
  starter_blocking_rpg_api/         ← blocking tournament API (your starting point)
  missions/                         ← 8 missions
  projects/                         ← P01 Async Quest Aggregator · P02 Background Report Queue · P03 boss fight
```

Each checkpoint project (`P01`, `P02`) is a standalone exercise that exercises the level's concepts.
The boss fight (`P03`) is a full-size challenge that combines everything from the level.

## Note on global commands

This repository contains intentionally incomplete starter files. Running
`uv run pytest` or `uv run ruff check .` at the start of the course will
show errors — that is expected. Starter files are meant to be incomplete
until you fill them in.

The correct workflow is always per-mission:

```bash
uv run python level_1_python_basics/missions/01_hero_stats/task.py    # run your code
uv run python level_1_python_basics/missions/01_hero_stats/check.py   # verify your solution
```

Global `pytest` and `ruff` are tools for the course author, not for students.
