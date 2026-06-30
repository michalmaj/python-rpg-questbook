# Mission 01: Hero Stats

## Goal

Store your hero's basic information using Python variables.

## You will learn

- How to create variables
- Basic data types: `str` and `int`
- How to build and return a dictionary

## Game problem

Every RPG hero needs stats: a name, hit points, attack damage, and gold.
We need a way to store all of this in one place so the rest of the game can use it.

## Your task

Open `task.py` and complete the function `get_hero_stats()`.

It should return a dictionary with these exact values:

| Key        | Value   | Type  |
|------------|---------|-------|
| `"name"`   | `"Ada"` | `str` |
| `"hp"`     | `100`   | `int` |
| `"damage"` | `15`    | `int` |
| `"gold"`   | `50`    | `int` |

**Reminder — how to build a dictionary:**

```python
my_dict = {
    "key": "value",
    "number": 42,
}
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

Add two more stats to your dictionary:

- `"level"` → start at `1`
- `"armor"` → start at `5`

Update the print block in `task.py` to display them.

---

Next mission: `missions/02_damage_and_healing/README.md`
