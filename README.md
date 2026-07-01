# Python RPG Questbook

Learn Python by building a real terminal RPG — one mechanic at a time.

## What is this?

This is a beginner Python course built around one growing story: you are building a terminal RPG game.

Each mission teaches one Python concept by adding a new game mechanic:

- variables store hero stats
- conditions decide who wins a battle
- loops run the combat
- files save the combat log
- data analysis asks: is the game balanced?

No abstract examples. Every line of code does something in the game.

## Setup

You need [uv](https://docs.astral.sh/uv/) installed. If you completed the setup course, you already have it.

```bash
git clone https://github.com/michalmaj/python-rpg-questbook.git
cd python-rpg-questbook
uv sync
uv run python main.py
```

## How to use this course

Open `COURSE_MAP.md` to see the full list of missions.

For each mission:

```bash
# 1. Read the mission instructions
#    Open: missions/01_hero_stats/README.md

# 2. Edit the task file
#    Open: missions/01_hero_stats/task.py

# 3. Run your code
uv run python missions/01_hero_stats/task.py

# 4. Check your solution
uv run python missions/01_hero_stats/check.py
```

## Track your progress

```bash
uv run python tools/course_status.py
```

## Course structure

```
missions/    ← short focused exercises (one concept each)
projects/    ← larger challenges that combine what you learned
tools/       ← helper scripts
```
