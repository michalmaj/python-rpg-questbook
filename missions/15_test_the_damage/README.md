# Mission 15: Test the Damage

## Goal

Write your first automated tests with pytest — then never wonder again if your combat math is broken.

## You will learn

- `def test_xxx():` — how pytest recognizes a test function
- `assert` in a test — what makes a test pass or fail
- `uv run pytest` — running all tests at once
- Reading red (FAILED) and green (PASSED) output

## Game problem

Every mission so far, you ran the script and eyeballed the output. That works for 15 lines of code. It breaks when the game has 1500 lines and you change one function — did you just break something three files away?

Automated tests answer that question instantly.

## Python concept

A **test** is a function that calls your code and asserts the result is what you expect:

```python
def test_apply_damage():
    result = apply_damage(100, 30)
    assert result == 70
```

pytest finds any function whose name starts with `test_`, runs it, and reports pass or fail.

Run all tests in a file:
```bash
uv run pytest missions/15_test_the_damage/test_combat.py -v
```

The `-v` flag shows each test name and its result:
```
PASSED test_combat.py::test_apply_damage
FAILED test_combat.py::test_apply_damage_floor
```

## Your task

Open `test_combat.py`. Each test function has a `...` where the expected value should go. Replace every `...` with the correct value.

For example:
```python
def test_apply_damage():
    result = apply_damage(100, 30)
    assert result == ...  # replace ... with 70
```

becomes:
```python
def test_apply_damage():
    result = apply_damage(100, 30)
    assert result == 70
```

There are 6 tests total. When all 6 pass, you're done.

## Run

Start with all tests failing (the `...` makes every assert false):

```bash
uv run pytest missions/15_test_the_damage/test_combat.py -v
```

Fix one test at a time and re-run. Watch the red list shrink.

## Check

```bash
uv run python missions/15_test_the_damage/check.py
```

## Side quest

pytest shows you what went wrong when a test fails. Try a deliberate mistake:

```python
assert result == 999
```

Run pytest and read the failure output:

```
AssertionError: assert 70 == 999
```

pytest tells you the actual value (`70`) and what you asserted (`999`). This is the core debugging loop: write a test, run it, read the failure, fix the code or the test.

## Break it

Change `max(0, hp - damage)` in `combat.py` to just `hp - damage`. Run the tests:

```
FAILED test_apply_damage_floor - assert -30 == 0
```

One broken line, one failing test — immediately visible. This is why tests exist.

## Fix it

Restore `max(0, hp - damage)`. All tests go green again.

## Real-world translation

Every serious Python project has a `tests/` folder. Before code ships, the full test suite runs automatically (CI). If any test fails, the deploy is blocked. The tests you just wrote are exactly the kind that would run in production CI for a real game backend.

---

Next mission: `projects/04_full_rpg/README.md`
