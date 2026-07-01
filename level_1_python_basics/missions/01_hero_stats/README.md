# Mission 01: Hero Stats

## Goal

Store your hero's basic information using Python variables.

## You will learn

- How to create variables
- Basic data types: `str` and `int`
- How to print values with f-strings

## Game problem

Every RPG hero needs stats: a name, hit points, attack damage, and gold.
We need to give each of these a name and a value so the rest of the game can use them.

## Your task

Open `task.py`. You will see four variables, each set to `None`.
Replace each `None` with the correct value:

| Variable      | Value   | Type  |
|---------------|---------|-------|
| `hero_name`   | `"Ada"` | `str` |
| `hero_hp`     | `100`   | `int` |
| `hero_damage` | `15`    | `int` |
| `hero_gold`   | `50`    | `int` |

**Reminder — variables in Python:**

```python
hero_name = "Ada"    # text (string) — always in quotes
hero_hp = 100        # whole number (int) — no quotes
```

## Run

See your hero stats printed:

```bash
uv run python missions/01_hero_stats/task.py
```

## Check

Verify your solution:

```bash
uv run python missions/01_hero_stats/check.py
```

You should see:
```
✅ Mission 01 complete: Hero Stats
```

## Side quest

Add two more variables:

- `hero_level = 1`
- `hero_armor = 5`

Update the `print` lines in `task.py` to display them too.

---

Next mission: `level_1_python_basics/missions/02_damage_and_healing/README.md`
