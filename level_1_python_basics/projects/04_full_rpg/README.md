# Project 04: Full Terminal RPG

## Boss Fight — World 4: Saving and Structure

You have the tools. Now build the complete game.

This project combines everything from World 4:

| Skill | Mission |
|-------|---------|
| Hero dataclass | Mission 14 |
| Combat module  | Mission 13 |
| Random damage  | Mission 09 |
| JSON save file | Mission 12 |
| CSV combat log | Mission 11 |

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

## Your tasks

Open `rpg.py`. Complete the five TODOs in order:

**TODO 1** — Create a Hero by uncommenting one of the three class lines.

**TODO 2** — Write the combat loop using `is_alive()`, `roll_damage()`, and `apply_damage()` from `combat.py`. Append `[round_number, hero.hp, boss_hp]` to `combat_log` each round.

**TODO 3** — After the loop, print who won.

**TODO 4** — Save the hero's final state to `save_game.json`.

**TODO 5** — Write `combat_log` to `combat_log.csv` with header `round,hero_hp,boss_hp`.

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

The check verifies: hero name in output, combat rounds printed, result printed, `save_game.json` has the right keys, `combat_log.csv` has the right header and at least one data row.

## Side quest

The combat log is the bridge to Part 2. After you finish, try opening it in Python:

```python
import csv
with open("combat_log.csv") as f:
    for row in csv.reader(f):
        print(row)
```

In Part 2 (Mission 18), you will load this exact file with Pandas and plot the hero's HP over time.

## Challenge

Add a healing potion. Every 3 rounds, the hero drinks a potion and heals 20 HP (capped at `max_hp`). Use `apply_healing()` from `combat.py`.

---

*You have completed World 4. Next: `level_1_python_basics/missions/16_dice_are_data/README.md`*
