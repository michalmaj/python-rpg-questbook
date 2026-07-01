# Mission 09: Pure Functions

## Goal

Extract combat logic into pure functions — functions that take inputs and return outputs without side effects.

## You will learn

- What makes a function "pure"
- Why pure functions are easier to test and reuse
- How to separate calculation from I/O (printing, file writing)
- The concept of side effects

## Game problem

In the legacy RPG, `hero_attacks()` does four things at once:
1. Calculates damage
2. Mutates `monster["hp"]`
3. Prints to the terminal
4. Appends to the combat log

```python
def hero_attacks(monster):
    dmg = hero_atk + roll(6) - monster["def"]
    if dmg < 1:
        dmg = 1
    print(f"{hero_name} attacks for {dmg} damage.")    # side effect
    monster["hp"] -= dmg                               # side effect
    log_rows.append(...)                               # side effect
```

You cannot test the damage calculation without also testing the print output and the log. It is all tangled together.

**Pure function:** given the same inputs, always returns the same kind of output. No printing, no mutation, no global state.

## Python concept

A **pure function** is a function with no side effects — it only takes arguments and returns a value.

```python
# Impure — prints and mutates global state
def attack(monster):
    dmg = hero_attack - monster["def"]
    monster["hp"] -= dmg           # mutation
    print(f"Deals {dmg} damage")   # I/O
    global log
    log.append(dmg)                # global mutation

# Pure — takes inputs, returns output
def compute_damage(atk: int, def_: int, dice_roll: int) -> int:
    return max(1, atk + dice_roll - def_)
```

Now you can test `compute_damage(15, 5, 4)` == `14` without any printing or setup. The caller decides what to do with the result.

## Your task

Open `task.py`. You will find an impure `hero_attacks()` function extracted from the legacy code. Your job is to extract the damage calculation into a pure `compute_damage(atk, def_, dice_roll)` function, and a separate `resolve_hit(hero_atk, monster_def)` function that calls `compute_damage` with a real dice roll.

## Run

```bash
uv run python level_2_oop_and_design/missions/09_pure_functions/task.py
```

## Check

```bash
uv run python level_2_oop_and_design/missions/09_pure_functions/check.py
```

## Break it on purpose

Add `print("computing...")` inside `compute_damage`. Run the check. Does it still pass? Now ask yourself: what happens in production when 10,000 battles run in simulation mode?

## Fix it

Remove the `print`. Pure functions do not produce output. The caller decides whether to print, log, or ignore.

## Side quest

Write a `simulate_battle(hero_atk, hero_def, monster_atk, monster_def, rounds)` function that runs `rounds` combat turns and returns `(hero_hp_remaining, monster_hp_remaining)`. No printing — just math. This is how game balance tools work.

## Real-world translation

Functional programming, React's pure components, Redux reducers, database query builders — all rely on pure functions because they are predictable, testable, and composable.

## Checklist

- [ ] I can identify side effects in a function (printing, mutation, I/O)
- [ ] I can extract a pure calculation from an impure function
- [ ] I understand that pure functions are easier to test
- [ ] I know that the caller handles I/O — the function just returns a value
- [ ] I can pass a dice roll as an argument to make randomness testable

---

Next mission: `level_2_oop_and_design/missions/10_add_tests/README.md`
