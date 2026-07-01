# Python RPG Questbook

Learn Python by building a real terminal RPG — one mechanic at a time.

## What is this?

This is a Python course built around one growing story: you are building a terminal RPG game.

Each mission teaches one Python concept by adding a new game mechanic:

- variables store hero stats
- conditions decide who wins a battle
- loops run the combat
- files save the combat log
- data analysis asks: is the game balanced?

The course continues into professional Python territory — OOP, validation, persistence, and clean architecture — using the same RPG as the vehicle.

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

```
level_1_python_basics/              ← Python fundamentals through terminal RPG + data analysis
  missions/                         ← 20 focused exercises (one concept each)
  projects/                         ← boss fights that combine what you learned

level_2_oop_and_design/             ← OOP, refactoring, design patterns
  starter_legacy_rpg/               ← the code you will clean up
  missions/                         ← 10 missions
  projects/                         ← boss fight: refactored RPG

level_3_validation_and_persistence/ ← Pydantic, repository pattern, SQLite
  starter_raw_rpg/                  ← the code you will harden
  missions/                         ← 7 missions
  projects/                         ← boss fight: SQLite backend

level_4_interfaces/                 ← CLI, logging, Rich output, reports, entry points
  starter_verbose_rpg/              ← the interface-smelly app you will improve
  missions/                         ← 6 missions
  projects/                         ← boss fight: installable CLI tool

tools/                              ← helper scripts (course_status, author_check)
```

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
