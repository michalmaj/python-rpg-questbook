# Project 01: Battle Calculator

**Boss Fight — World 1**

> Requires: Mission 01, Mission 02, Mission 03

## Goal

Combine everything from Missions 01–03 into a small interactive battle simulator.
No functions — just a single script that runs from top to bottom.

## What you will build

A terminal program where the player:

1. Chooses a hero class (warrior / mage / rogue)
2. Sees their starting stats
3. Takes damage from a monster
4. Optionally heals with a potion
5. Sees a battle summary

## Your task

Open `battle_calculator.py`. Fill in four `TODO` sections:

| Step | What to do |
|------|-----------|
| 1 | Set `hero_name`, `hero_hp`, `hero_damage` using `if` / `elif` / `else` — same pattern as Mission 03 |
| 2 | Calculate `hero_hp` after `monster_damage`. HP cannot go below `0` — same pattern as Mission 02 |
| 3 | Calculate `hero_hp` after `potion_heal`. HP cannot exceed `max_hp` — same pattern as Mission 02 |
| 4 | Print the right summary: survived or fallen — use the f-string patterns from Mission 01 |

## Run

```bash
uv run python projects/01_battle_calculator/battle_calculator.py
```

## Check

```bash
uv run python projects/01_battle_calculator/check.py
```

---

Next: `uv run python tools/course_status.py` — then continue with `COURSE_MAP.md`
