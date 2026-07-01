# Mission 10: Add Tests

## Goal

Write pytest tests for the pure functions and classes you built in Level 2.

## You will learn

- Writing `test_` functions that pytest discovers automatically
- Testing pure functions with known inputs and expected outputs
- Testing class behaviour (methods, properties)
- What to test and what not to test
- The test pyramid: many unit tests, fewer integration tests

## Game problem

The legacy RPG has no tests. If you change the damage formula — or if a future teammate changes it — nothing tells you whether the game still works correctly. Tests do.

You have pure functions now. Pure functions are the easiest code to test: you give them inputs, they give you outputs, and you check that the output is what you expected.

## Python concept

pytest discovers any function whose name starts with `test_`:

```python
# test_combat.py
from combat import compute_damage

def test_compute_damage_normal():
    assert compute_damage(atk=15, def_=5, dice_roll=4) == 14

def test_compute_damage_minimum():
    assert compute_damage(atk=1, def_=100, dice_roll=1) == 1

def test_compute_damage_exact():
    assert compute_damage(atk=10, def_=3, dice_roll=6) == 13
```

Run: `uv run pytest`

Each `test_` function is one assertion about the code. If an assertion fails, pytest shows you exactly what went wrong.

## Your task

Open `test_combat.py`. You will find empty test stubs. Implement each test by filling in the assertion. The `compute_damage` function is imported from `combat.py` (provided and complete).

## Run

```bash
uv run pytest level_2_oop_and_design/missions/10_add_tests/ -v
```

## Check

```bash
uv run python level_2_oop_and_design/missions/10_add_tests/check.py
```

## Break it on purpose

Change `compute_damage` in `combat.py` to return `0` instead of `max(1, dmg)`. Run the tests. Which test fails first?

## Fix it

Restore `max(1, dmg)`. This is why tests exist — they catch regressions before players do.

## Side quest

Write tests for the `Hero` and `Monster` classes from Mission 03:
- Test that `take_damage` reduces HP correctly
- Test that `is_alive` returns `False` when HP reaches 0
- Test that HP never goes below 0 after many hits

## Real-world translation

Every serious Python project has a test suite. Django, FastAPI, NumPy, Pandas — all have thousands of tests that run on every commit. "If it's not tested, it's broken" is not an exaggeration.

## Checklist

- [ ] I can write a `test_` function that pytest discovers
- [ ] I can import a function from another file in a test
- [ ] I know that each test should check one specific behaviour
- [ ] I can run all tests with `uv run pytest`
- [ ] I understand that tests catch regressions — changes that break working code

---

**World 3 complete!** You are ready for the boss fight.

**Boss Fight:** `level_2_oop_and_design/projects/01_refactored_rpg/README.md`
