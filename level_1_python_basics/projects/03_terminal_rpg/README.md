# Project 03: Terminal RPG

**Boss Fight — World 3**

> Requires: Missions 01–10

## Goal

Build a complete terminal RPG battle — hero vs monster, round by round, with dice rolls.

## What you will build

A terminal program where:

1. The player chooses a hero class
2. The hero fights the Goblin King in a while loop
3. Each round uses random dice for damage (Mission 09 pattern)
4. The game ends when one side falls
5. A final message announces the winner

## Your task

Open `rpg.py`. Fill in three TODO sections:

| Step | What to do |
|------|-----------|
| 1 | Define `roll_damage(min_val, max_val)` — returns a random int in range (Mission 09) |
| 2 | Define `is_alive(hp)` — returns True if hp > 0 (Mission 08 pattern) |
| 3 | Set `hero` dict based on `hero_class` (Mission 07 + Mission 03 pattern) |
| 4 | Write the `while` loop — both sides attack each round (Mission 04 pattern) |

**Hero stats:**

| Class     | HP  | Damage range |
|-----------|-----|--------------|
| Warrior   | 120 | 10–20        |
| Mage      | 80  | 18–28        |
| Rogue     | 100 | 14–24        |

The Goblin King has 80 HP and deals 8–15 damage per round.

## Run

```bash
uv run python projects/03_terminal_rpg/rpg.py
```

## Check

```bash
uv run python projects/03_terminal_rpg/check.py
```

---

Next: `uv run python tools/course_status.py` — then continue with `COURSE_MAP.md`
