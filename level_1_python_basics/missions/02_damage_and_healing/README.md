# Mission 02: Damage and Healing

## Goal

Calculate how your hero's HP changes during combat.

## You will learn

- Arithmetic operators: `-`, `+`
- How to use `min()` and `max()` to keep a value in range
- Chaining calculations step by step

## Game problem

During a battle, the hero takes damage and sometimes drinks a potion to heal.
HP must stay between `0` (dead) and `max_hp` (full health).

## Your task

Open `task.py`. You will see three variables set to `None`.
Replace each `None` with the correct arithmetic expression:

| Variable           | What to calculate                                           | Expected |
|--------------------|-------------------------------------------------------------|----------|
| `hp_after_attack`  | `hero_hp` minus `monster_damage`. Cannot go below `0`.      | `70`     |
| `hp_after_healing` | `hp_after_attack` plus `potion_heal`. Cannot exceed `max_hp`. | `90`   |
| `hp_after_big_hit` | `hp_after_healing` minus `big_hit`. Cannot go below `0`.    | `0`      |

**How to clamp a value:**

```python
max(0, value)        # if value is negative, returns 0 instead
min(max_hp, value)   # if value exceeds max_hp, returns max_hp instead
```

## Run

```bash
uv run python missions/02_damage_and_healing/task.py
```

You should see the HP change after each event.

## Check

```bash
uv run python missions/02_damage_and_healing/check.py
```

## Side quest

Add a fourth calculation:

```python
second_hit = 15
hp_after_second_hit = ...  # hp_after_big_hit minus second_hit, cannot go below 0
```

Then add a print line to show `hp_after_second_hit`.

---

Next mission: `level_1_python_basics/missions/03_choose_your_hero/README.md`
