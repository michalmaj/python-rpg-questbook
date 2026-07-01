# Mission 13: Split the Game

## Goal

Move combat functions into their own module so other files can use them.

## You will learn

- `from module import name` — pull one name from another file
- `from module import a, b, c` — pull multiple names at once
- `if __name__ == "__main__":` — code that runs only when a file is run directly

## Game problem

Your combat functions (`apply_damage`, `apply_healing`, `is_alive`) live only in the file you defined them. Every new game file would need its own copy. That leads to bugs when one copy drifts from another.

The solution: put shared functions in their own file (`combat.py`) and import them wherever you need them.

## Python concept

A **module** is any `.py` file. When you import from it, Python executes the file and gives you access to its names:

```python
from combat import apply_damage
```

The `if __name__ == "__main__":` guard lets a file be both importable and runnable:

```python
# combat.py
def apply_damage(hp, damage):
    return max(0, hp - damage)

if __name__ == "__main__":
    # Only runs when you do: python combat.py
    # Does NOT run when another file does: from combat import apply_damage
    print(apply_damage(100, 30))  # 70
```

Without this guard, any code at the top level of `combat.py` would also run every time another file imports it — usually not what you want.

## Your task

**Step 1:** Open `combat.py`. Implement the three functions:

```python
def apply_damage(hp, damage):
    return max(0, hp - damage)

def apply_healing(hp, heal_amount, max_hp):
    return min(max_hp, hp + heal_amount)

def is_alive(hp):
    return hp > 0
```

**Step 2:** Open `task.py`. Remove the `#` from the import line:

```python
from combat import apply_damage, apply_healing, is_alive
```

## Run

Test `combat.py` directly to see the `if __name__ == "__main__":` guard in action:

```bash
uv run python missions/13_split_the_game/combat.py
```

Expected output:
```
70
90
False
```

Then run `task.py` to see the import in action:

```bash
uv run python missions/13_split_the_game/task.py
```

Expected output:
```
Hero HP:      90
Monster HP:   45
Hero alive:   True
Monster alive:True
```

## Check

```bash
uv run python missions/13_split_the_game/check.py
```

The check imports from `combat.py` directly and also runs `task.py` as a subprocess to confirm the import line is in place.

## Side quest

Try importing `combat` in the Python REPL and see what happens:

```bash
uv run python
```

```python
>>> import sys
>>> sys.path.insert(0, "missions/13_split_the_game")
>>> from combat import apply_damage
>>> apply_damage(100, 30)
70
```

This is exactly what `check.py` does internally.

## Break it

Comment out the import line in `task.py` again:

```python
# from combat import apply_damage, apply_healing, is_alive
```

Run `task.py`. You get `NameError: name 'apply_damage' is not defined`. This is what happens when you use a name without importing it — Python has no idea where to find it.

## Fix it

Uncomment the import line. Run again.

## Real-world translation

Every Python project uses modules. `import json`, `import random`, `from pathlib import Path` — all of these pull names from other files (the standard library). Your own code works the same way.

---

Next mission: `missions/14_hero_dataclass/README.md`
