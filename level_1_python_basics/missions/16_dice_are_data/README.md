# Mission 16: Dice Are Data

## Goal

Roll 1000 dice in one line and analyze the results with NumPy.

## You will learn

- `import numpy as np` — the convention for importing NumPy
- `np.random.randint(low, high, size)` — generate many random numbers at once
- `array.sum()`, `array.mean()`, `array.min()`, `array.max()` — instant statistics
- The key difference between a Python list and a NumPy array

## Game problem

In Mission 09 you rolled one die with `random.randint(1, 6)`. One roll tells you nothing about a weapon — you need to know its *average* damage and how consistent it is.

NumPy lets you simulate 1000 rolls in a single line and get the statistics instantly. This is how game designers test whether a weapon is balanced.

## Python concept

A **NumPy array** is a list of numbers optimized for math. The key difference from a Python list:

```python
# Python list — math requires a loop
rolls = [3, 1, 6, 2, 5]
total = sum(rolls)       # built-in sum

# NumPy array — math is a method call, and works on 1 million items just as fast
import numpy as np
rolls = np.array([3, 1, 6, 2, 5])
total = rolls.sum()      # same result, same syntax — but scales to millions
```

Generating many random numbers at once:

```python
rolls = np.random.randint(1, 7, size=1000)
#                         ^  ^  ^^^^
#                     low  high  count
#                         (exclusive!)
```

`high` is **exclusive** — to get values 1 through 6, you write `randint(1, 7, ...)`.

## Your task

Open `task.py`. Complete the five TODOs:

1. `rolls` — array of 1000 d6 rolls (values 1–6)
2. `total_damage` — sum of all rolls
3. `average_roll` — mean of all rolls
4. `min_roll` — lowest roll
5. `max_roll` — highest roll

Expected output (values vary each run):
```
Rolls (first 10): [3 5 1 6 2 4 3 6 1 5]
Total damage:     3487
Average roll:     3.49
Min roll:         1
Max roll:         6
```

## Run

```bash
uv run python missions/16_dice_are_data/task.py
```

Run it several times — the totals change, but the average always hovers near 3.5.

## Check

```bash
uv run python missions/16_dice_are_data/check.py
```

## Side quest

Compare two weapons — a d6 (1–6) and a d4+1 (2–5):

```python
d6   = np.random.randint(1, 7, size=10000)
d4p1 = np.random.randint(2, 6, size=10000)

print(f"d6   — avg: {d6.mean():.2f}, min: {d6.min()}, max: {d6.max()}")
print(f"d4+1 — avg: {d4p1.mean():.2f}, min: {d4p1.min()}, max: {d4p1.max()}")
```

Same average (3.5), different range. Which weapon do you prefer as a game designer?

## Break it

Change `size=1000` to `size=0`. Run the check — what error do you get? Try `size="banana"` next. NumPy gives specific error messages for type mismatches.

## Real-world translation

NumPy is the foundation of scientific Python. Pandas, Matplotlib, TensorFlow, and PyTorch all use NumPy arrays internally. The `.mean()`, `.min()`, `.max()` methods you just used are the same ones data scientists run on million-row datasets every day.

---

Next mission: `missions/17_damage_distributions/README.md`
