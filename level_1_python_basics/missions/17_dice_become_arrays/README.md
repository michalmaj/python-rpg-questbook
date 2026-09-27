# Mission 17: Dice Become Arrays

## Goal

See exactly what changes — and what doesn't — when a collection of numbers
becomes a NumPy array instead of a Python list.

## Game problem

You already have dice rolls from Mission 10. To answer questions like
"what's the average roll?" or "double every roll for a weekend event,"
plain Python needs a loop every time. NumPy does math directly on the
whole collection, in one step.

## Python concept

A Python list and a NumPy array are **different data types** — not the
same thing with a faster engine underneath. The clearest way to see this
is what `*` does to each one:

```python
gold_pickups = [10, 25, 5, 40]
gold_pickups * 2
# [10, 25, 5, 40, 10, 25, 5, 40]  <- the list repeats itself

import numpy as np
gold_array = np.array(gold_pickups)
gold_array * 2
# [20 50 10 80]  <- every value is doubled
```

Same syntax, same `* 2`, completely different result. A NumPy array is a
collection of values built for element-by-element math — every operation
you write applies to every element at once. That's why it exists: not
because it's "a faster list," but because `*`, `+`, and friends mean
something different on it by design.

Two more things worth knowing about an array from the start:

- `.shape` — how many elements it holds
- `.dtype` — what kind of values it holds (whole numbers, decimals, ...)

## Your task

Open `task.py`. Work through it top to bottom:

1. Turn a small, fixed list of 4 rolls into a NumPy array.
2. Check its `shape` and `dtype`.
3. Double every roll in one operation (element-wise, array → array).
4. Add a flat +1 bonus to every roll (array + scalar).
5. Compute the total, average, lowest, and highest roll.
6. Only then, generate 1000 random rolls with `np.random.randint(...)` and
   repeat the same four aggregations at that scale.

The first array only has 4 values — work out `doubled`, `buffed`, and the
aggregations by hand before you run the file, then check yourself.

## Run

```bash
uv run python missions/17_dice_become_arrays/task.py
```

## Check

```bash
uv run python missions/17_dice_become_arrays/check.py
```

## Side quest

The list-comprehension version of "double every roll" is:

```python
doubled_list = [roll * 2 for roll in rolls_list]
```

Compare it with `rolls * 2` on the array — same result, no loop, no `for`.

Then compare two weapons at 10 000 rolls each — a d6 (1–6) and a d4+1 (2–5):

```python
d6   = np.random.randint(1, 7, size=10000)
d4p1 = np.random.randint(2, 6, size=10000)
print(d6.mean(), d4p1.mean())   # close to each other
print(d6.max(), d4p1.max())     # not close at all
```

---

Next mission: `level_1_python_basics/missions/18_critical_hits/README.md`
