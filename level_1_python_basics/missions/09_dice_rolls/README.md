# Mission 09: Dice Rolls

## Goal

Make combat unpredictable — every attack rolls a die.

## You will learn

- `import` — load a module from Python's standard library
- `random.randint(a, b)` — generate a random integer from `a` to `b` (both included)
- Why random output requires testing ranges instead of exact values

## Game problem

Fixed damage values make combat boring and predictable.
Real RPGs roll dice — so each fight plays out differently.
Python's `random` module gives us that die.

## Your task

Open `task.py`. It already has `import random` at the top.
Fill in the four `None` values.

**How to use random:**

```python
import random            # load the random module

roll = random.randint(1, 6)   # random integer: 1, 2, 3, 4, 5, or 6
```

`random.randint(a, b)` includes both endpoints — a 6-sided die gives 1–6, a 4-sided die gives 1–4.

| Variable        | What to assign                     |
|-----------------|------------------------------------|
| `hero_roll`     | `random.randint(1, 6)` — d6        |
| `hero_damage`   | `hero_roll * 3`                    |
| `monster_roll`  | `random.randint(1, 4)` — d4        |
| `monster_damage`| `monster_roll * 2`                 |

## Run

```bash
uv run python missions/09_dice_rolls/task.py
```

The numbers will be different each time — that's the point!

## Check

The check cannot know the exact roll, so it verifies two things instead:
1. The roll is within the correct range (1–6 for the hero, 1–4 for the monster)
2. The damage equals the roll times the multiplier

```bash
uv run python missions/09_dice_rolls/check.py
```

## Side quest

`random.choice()` picks a random item from a list:

```python
attack_type = random.choice(["slash", "magic bolt", "crit"])
print(f"Hero uses {attack_type}!")
```

Add an attack type to your combat output. Run it a few times to see different results.

---

Next mission: `level_1_python_basics/missions/10_safe_input/README.md`
