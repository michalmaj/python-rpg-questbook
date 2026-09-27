# Mission 09: Shared Inventory

## Goal

Find and fix a bug that catches every Python beginner at least once: two
names pointing at the same list.

## You will learn

- Why `list_b = list_a` does not create a copy
- How this bug can hide inside an ordinary function call
- `.copy()` — the simplest way to make an independent copy of a flat list

## Game problem

The party leader wants to hand out identical starting kits to new recruits.
Copying a list looks like it should be as simple as `recruit_kit = starter_kit`
— but that line doesn't make a copy at all.

## Python concept

A variable name doesn't hold a list — it points to one. `list_b = list_a`
makes `list_b` point to the *same* list as `list_a`. There is still only one
list in memory, now with two names attached to it. Changing it through
either name changes what you see through both.

This is different from a plain number: `b = a` for an `int` makes `b` an
independent value, because ints can't be changed in place at all. Lists can
— and that's where the surprise comes from.

## Your task

Open `task.py`. Part 1 is already complete — run it and read the output
carefully before changing anything. Then fix Part 2: give the recruit a
real, independent copy of the kit using `.copy()` (or `list(...)`, or
`[:]` — all three work the same way on a flat list like this one).

## Run

```bash
uv run python missions/09_shared_inventory/task.py
```

Read the "Starter kit" lines from Part 1 first — that's the exact bug
you're fixing in Part 2.

## Check

```bash
uv run python missions/09_shared_inventory/check.py
```

## Note on deeper copies

`.copy()` works here because every item in the kit is a plain string. If a
list contained other lists or dicts instead, `.copy()` would only copy the
outer list — the inner ones would still be shared. That situation needs a
different tool, outside the scope of this mission.

---

Next mission: `level_1_python_basics/missions/10_dice_rolls/README.md`
