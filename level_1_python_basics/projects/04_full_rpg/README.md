# Project 04: Full Terminal RPG

## Boss Fight — World 4: Saving and Structure

You have the tools. Now build the complete game.

This project combines everything from World 4:

| Skill | Mission |
|-------|---------|
| Hero dataclass | Mission 15 |
| Combat module  | Mission 14 |
| Random damage  | Mission 10 |
| JSON save file | Mission 13 |
| CSV combat log | Mission 12 |

## What you build

A terminal RPG where:
- The player names their hero and picks a class
- Hero fights a boss in a while loop until one side reaches 0 HP
- The result is saved to `save_game.json`
- Every round is logged to `combat_log.csv`

## Files

| File | Your role |
|------|-----------|
| `combat.py` | Given — import from it |
| `rpg.py` | Edit — 5 TODOs to complete |
| `check.py` | Run to verify |

## Available pieces

`combat.py` is given — import what you need from it:

- `roll_damage(min_val, max_val)` — random damage in range
- `apply_damage(hp, damage)` — subtract damage, floored at 0
- `apply_healing(hp, heal_amount, max_hp)` — add HP, capped at max
- `is_alive(hp)` — `True` if hp > 0

`rpg.py` has the `Hero` dataclass already defined, and reads the hero's
name from `input()`. Five things are still missing — see the TODOs in
the file for the exact requirements. In short: create the `Hero`, run
the fight to completion, report the result, and persist it to both
`save_game.json` and `combat_log.csv`.

If you need a reminder of the JSON/CSV syntax itself, look back at
Missions 11 and 12 — the mechanics here are the same, just applied to
this game's own data instead of the mission's example data.

## Run

```bash
uv run python projects/04_full_rpg/rpg.py
```

Example session:
```
Enter your hero's name: Ada

Ada the Warrior faces the Shadow Dragon!
----------------------------------------
Round 1: Ada deals 17 | Shadow Dragon deals 14 | Hero HP: 106 | Boss HP: 133
Round 2: Ada deals 12 | Shadow Dragon deals 18 | Hero HP: 88  | Boss HP: 121
...
Ada wins! The Shadow Dragon is defeated.
```

Then inspect what was written:

```bash
cat save_game.json
cat combat_log.csv
```

## Check

```bash
uv run python projects/04_full_rpg/check.py
```

The check doesn't just look for the right keys or headers — it recomputes
the expected damage ranges from your chosen class and the boss's stats,
and verifies every round in `combat_log.csv` actually falls within them.
It also checks that `save_game.json`'s final HP matches the CSV's last
row — both files have to describe the same finished game.

## Side quest

The combat log is the bridge to Part 2. After you finish, try opening it in Python:

```python
import csv
with open("combat_log.csv") as f:
    for row in csv.reader(f):
        print(row)
```

In Part 2 (Mission 21), you will load this exact file with Pandas and plot the hero's HP over time.

## Challenge

Add a healing potion. Every 3 rounds, the hero drinks a potion and heals 20 HP (capped at `max_hp`). Use `apply_healing()` from `combat.py`.

---

*You have completed World 4. Next: `level_1_python_basics/missions/17_dice_become_arrays/README.md`*
