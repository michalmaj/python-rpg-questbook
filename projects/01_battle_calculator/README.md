# Project 01: Battle Calculator

**Boss Fight — World 1**

> Requires: Mission 01, Mission 02, Mission 03

## Goal

Combine everything from Missions 01–03 into a small interactive battle simulator.

## What you will build

A terminal program where the player:

1. Chooses a hero class (warrior / mage / rogue)
2. Sees their starting stats
3. Takes damage from a monster
4. Optionally heals with a potion
5. Sees a battle summary

## Your task

Open `battle_calculator.py`. Complete the four functions marked with `TODO`:

| Function | What it does |
|----------|-------------|
| `get_hero_stats(hero_class)` | Returns stats for the chosen class, or `None` if unknown |
| `calculate_damage(hero_hp, damage)` | Reduces HP (minimum 0) |
| `calculate_healing(hero_hp, heal_amount, max_hp)` | Restores HP (maximum `max_hp`) |
| `summarize_battle(hero_class, final_hp)` | Returns a summary string |

You have already written similar logic in Missions 01–03. This time, you are putting it all together.

## Run

```bash
uv run python projects/01_battle_calculator/battle_calculator.py
```

## Check

```bash
uv run python projects/01_battle_calculator/check.py
```

## Tests

These are the same checks, written in a more professional style. Come back to these after Mission 15 when you learn about pytest:

```bash
uv run pytest projects/01_battle_calculator -v
```

## Side quest

Add a `calculate_gold_reward(monster_level: int) -> int` function.
It should return `monster_level * 10` gold.
Print the gold reward after the battle summary.

---

Next: `uv run python tools/course_status.py` — then continue with `COURSE_MAP.md`
