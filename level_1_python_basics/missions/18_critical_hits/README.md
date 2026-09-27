# Mission 18: Critical Hits

## Goal

Pull specific values out of an array based on a condition — without
writing a single loop.

## Game problem

You have eight attack rolls from the last fight and want to know: which
ones were critical hits? Checking each value by hand doesn't scale past a
handful of rolls. NumPy lets you ask the whole array the question at once.

## Python concept

Comparing an array to a value produces a new array of `True`/`False`
values — one per element, same shape as the original. This is called a
**boolean mask**.

```python
gold_found = np.array([10, 0, 15, 0, 40])
found_gold = gold_found > 0
# [ True False  True False  True]
```

`found_gold` has exactly 5 values, same as `gold_found` — position by
position, it answers "was gold found here?" A mask on its own is just
`True`/`False`. The useful part is using it to index the original array:

```python
gold_found[found_gold]
# [10 15 40]   <- only the positions where the mask was True
```

And since `True` counts as `1` and `False` as `0`, summing a mask counts
how many positions matched:

```python
found_gold.sum()   # 3
```

## Your task

Open `task.py`. Part 1 asks for a boolean mask on the attack rolls, the
values it selects, and a count. Part 2 asks for the same three things on a
different array with a different condition.

## Run

```bash
uv run python missions/18_critical_hits/task.py
```

## Check

```bash
uv run python missions/18_critical_hits/check.py
```

## Side quest

Combining two conditions on an array needs `&` (not Python's `and`), and
each side needs its own parentheses:

```python
(attack_rolls > 3) & (attack_rolls < 6)
```

Try it on `attack_rolls` — which rolls count as "medium" by that
definition? Not required to complete the mission.

## Looking ahead

A boolean mask is exactly the idea behind filtering rows in a Pandas table
later in this course — `df[df["damage"] > 20]` works because of the same
True/False-per-position logic you just used here.

---

Next mission: `level_1_python_basics/missions/19_party_damage_grid/README.md`
