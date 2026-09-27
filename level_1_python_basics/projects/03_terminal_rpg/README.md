# Project 03: Terminal RPG

**Boss Fight — World 3**

> Requires: Missions 01–11

## Goal

Build a complete terminal RPG battle — hero vs monster, round by round, with dice rolls.

## What you will build

A terminal program where:

1. The player chooses a hero class
2. The hero fights the Goblin King in a while loop
3. Each round uses random dice for damage (Mission 10 pattern)
4. The game ends when one side falls
5. A final message announces the winner

## Requirements

Open `rpg.py`. Three functions need implementing:

**`roll_damage(min_val, max_val)`** — a random integer in that range, inclusive on both ends.

**`create_hero(hero_class)`** — returns the matching stats dict, or `None` for an unrecognized class:

| Class     | HP  | Damage range |
|-----------|-----|--------------|
| Warrior   | 120 | 10–20        |
| Mage      | 80  | 18–28        |
| Rogue     | 100 | 14–24        |

**`run_battle(hero, monster)`** — runs full rounds until one side's HP
reaches 0. Each round, both sides attack once, dealing a random amount of
damage within their own range. Print the round state as you go. Return
`(hero_hp, monster_hp, round_number)` when it's over.

The Goblin King has 80 HP and deals 8–15 damage per round.

Everything else — reading the class choice, calling these three
functions, printing the result — is already wired up at the bottom of
the file.

## Run

```bash
uv run python projects/03_terminal_rpg/rpg.py
```

## Check

The check calls your functions directly with many different inputs — including
fixed random seeds, so a battle's outcome is reproducible instead of
depending on luck.

```bash
uv run python projects/03_terminal_rpg/check.py
```

---

Next: `uv run python tools/course_status.py` — then continue with `COURSE_MAP.md`
