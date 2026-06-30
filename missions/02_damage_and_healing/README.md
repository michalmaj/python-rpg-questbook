# Mission 02: Damage and Healing

## Goal

Write functions that update your hero's HP during combat.

## You will learn

- Arithmetic operators: `-`, `+`
- How to use `min()` and `max()` to clamp a value within a range
- How to write functions with multiple parameters and a return value

## Game problem

During a battle, the hero takes damage and sometimes drinks a potion to heal.
HP must stay between `0` (dead) and `max_hp` (full health).
We need two functions that handle both changes correctly.

## Your task

Open `task.py` and complete two functions.

### apply_damage

```python
def apply_damage(hero_hp: int, damage: int) -> int:
```

Subtract `damage` from `hero_hp`. HP cannot go below `0`.

**Examples:**
- `apply_damage(100, 30)` → `70`
- `apply_damage(20, 50)` → `0` (not `-30`)

**Hint:** `max(0, value)` returns `0` if `value` is negative.

### apply_healing

```python
def apply_healing(hero_hp: int, heal_amount: int, max_hp: int) -> int:
```

Add `heal_amount` to `hero_hp`. HP cannot exceed `max_hp`.

**Examples:**
- `apply_healing(70, 20, 100)` → `90`
- `apply_healing(90, 20, 100)` → `100` (not `110`)

**Hint:** `min(max_hp, value)` returns `max_hp` if `value` is too high.

## Run

```bash
uv run python missions/02_damage_and_healing/task.py
```

## Check

```bash
uv run python missions/02_damage_and_healing/check.py
```

## Side quest

Write a third function:

```python
def is_alive(hero_hp: int) -> bool:
    ...
```

Return `True` if `hero_hp > 0`, and `False` otherwise.
Add a print to `task.py` that shows whether the hero is still alive after each attack.

---

Next mission: `missions/03_choose_your_hero/README.md`
