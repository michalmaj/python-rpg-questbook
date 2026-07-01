# Mission 08: Attack Function

## Goal

Write reusable functions so the damage formula lives in one place.

## You will learn

- `def` — define a named, reusable block of code
- Parameters — the variables a function receives as input
- `return` — send a value back to the caller
- Why functions beat copy-pasting

## Game problem

In Missions 02, 04, and 05 you wrote `max(0, hp - damage)` in multiple places.
If you wanted to add armor that reduces damage by 10%, you'd have to find every copy.
A function lets you write the logic once and call it by name everywhere:

```python
hp = apply_damage(hp, 30)   # readable
hp = apply_damage(hp, 200)  # same logic, different numbers
```

## Your task

Open `task.py` and define two functions above the "Use your functions" section.

**Function syntax:**

```python
def function_name(parameter1, parameter2):
    result = ...      # compute something
    return result     # send it back
```

### apply_damage

```python
def apply_damage(hero_hp, damage):
    # return hero_hp minus damage, never below 0
```

**Examples:**
- `apply_damage(100, 30)` → `70`
- `apply_damage(20, 50)` → `0` (not `-30`)

### apply_healing

```python
def apply_healing(hero_hp, heal_amount, max_hp):
    # return hero_hp plus heal_amount, never above max_hp
```

**Examples:**
- `apply_healing(70, 20, 100)` → `90`
- `apply_healing(90, 20, 100)` → `100` (not `110`)

## Run

```bash
uv run python missions/08_attack_function/task.py
```

Expected output:
```
After 30 damage:    70
After healing 20:   90
After overkill:     0
```

## Check

```bash
uv run python missions/08_attack_function/check.py
```

## Side quest

Python supports optional type hints that describe what a function expects and returns:

```python
def apply_damage(hero_hp: int, damage: int) -> int:
    return max(0, hero_hp - damage)
```

Add type hints to both functions. The code runs identically — hints are just documentation for readers (and tools like your editor).

---

Next mission: `level_1_python_basics/missions/09_dice_rolls/README.md`
