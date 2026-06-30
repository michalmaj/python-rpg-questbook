# Python RPG Questbook

A quest-based Python course for students: from the first script to a small terminal RPG, and then from game logs to basic data analysis with NumPy, Pandas, and Matplotlib.

## Project idea

This course teaches Python through one growing narrative: building a simple terminal RPG / battle arena.

Instead of isolated examples like:

```python
a = 42
```

students work with meaningful game state:

```python
hero_hp = 42
damage = 13
hero_hp = hero_hp - damage
```

Each Python concept adds something to the game:

- variables describe hero stats,
- conditions define game rules,
- loops create turn-based combat,
- lists store inventory and enemies,
- dictionaries describe characters and monsters,
- functions implement actions,
- files save combat logs,
- JSON stores save games,
- CSV logs become data for analysis.

The second part of the course introduces NumPy, Pandas, and Matplotlib through dice simulations, combat logs, D&D-style character statistics, and game balance analysis.

## Learning path

```text
Python setup and tools
        ↓
Python RPG Questbook
        ↓
Modern Python project structure
        ↓
Data, experiments, and ML projects
```

This repository is the missing middle step between learning the tools and working on larger Python/data/ML projects.

## Course parts

### Part 1: Python Core through Terminal RPG

Students build a small terminal game step by step:

1. first script,
2. variables and types,
3. input,
4. conditions,
5. loops,
6. lists,
7. dictionaries,
8. functions,
9. random dice rolls,
10. files and CSV,
11. JSON saves,
12. modules,
13. dataclasses,
14. simple tests,
15. mini project: Terminal RPG Battle Arena.

### Part 2: Game Data Analysis

Students analyze game data:

1. NumPy dice simulations,
2. damage distributions,
3. weapon comparison,
4. Pandas combat logs,
5. filtering and grouping,
6. Matplotlib charts,
7. final report: is the game balanced?

## Current status

This is an early project skeleton.

The first implementation goal is not to build the entire course at once. The first goal is to create a small, coherent vertical slice:

1. Mission 01: first script with hero stats.
2. Mission 02: variables for HP, damage, and gold.
3. Mission 03: input for hero name/class.
4. Mission 04: conditions for battle status.
5. A tiny playable combat prototype in the terminal.

## Development

This project uses `uv`.

Run the starter script:

```bash
uv run python main.py
```

Run checks later, when tests are added:

```bash
uv run pytest
```

Format/lint later, when the codebase grows:

```bash
uv run ruff check .
uv run ruff format .
```

## For AI agents

Before making changes, read:

```text
AGENT_BRIEF.md
```

That file describes the course vision, teaching style, constraints, and preferred direction.
