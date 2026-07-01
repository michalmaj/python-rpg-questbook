# Mission 05: pytest Parametrize

## Goal

Stop copy-pasting near-identical tests. Use `@pytest.mark.parametrize` to run one test function across many input/output combinations.

---

## Game Problem

You have a `compute_damage` function. You want to test it with five different stat combinations. Without parametrize, you write five nearly-identical functions — a maintenance nightmare. If the function signature changes, you update five places. If you find a bug, you wonder whether the other four cases actually cover different logic.

`@pytest.mark.parametrize` solves this: write the test once, declare the cases as data.

---

## Python Concept

### `@pytest.mark.parametrize`

```python
@pytest.mark.parametrize("atk,def_,roll,expected", [
    (10, 5, 3, 8),
    (5, 10, 1, 1),
    (20, 0, 6, 26),
])
def test_compute_damage(atk: int, def_: int, roll: int, expected: int) -> None:
    assert compute_damage(atk, def_, roll) == expected
```

One function, three test cases. pytest runs them all separately.

### `ids=` — readable test names

Without `ids=`, pytest generates names like `test_compute_damage[10-5-3-8]`. With `ids=`:

```python
@pytest.mark.parametrize("atk,def_,roll,expected", [
    (10, 5, 3, 8),
    (5, 10, 1, 1),
], ids=["normal_hit", "min_damage"])
def test_compute_damage(atk: int, def_: int, roll: int, expected: int) -> None:
    assert compute_damage(atk, def_, roll) == expected
```

Now failure output shows `FAILED test_combat.py::test_compute_damage[normal_hit]` — instantly readable.

### `pytest.mark.skip` and `pytest.mark.xfail`

```python
@pytest.mark.skip(reason="not implemented yet")
def test_future_feature() -> None:
    ...

@pytest.mark.xfail(reason="known bug — hero can deal 0 damage on exact tie")
def test_zero_damage_edge_case() -> None:
    assert compute_damage(5, 5, 0) >= 1
```

`skip` — skip this test entirely.
`xfail` — expect it to fail; pytest won't count it as a failure until it unexpectedly passes.

---

## Minimal Example

```python
import pytest
from rpg import compute_damage

@pytest.mark.parametrize("atk,def_,roll,expected", [
    (10, 5, 3, 8),   # normal: 10 + 3 - 5 = 8
    (5, 10, 1, 1),   # minimum: max(1, 5 + 1 - 10) = max(1, -4) = 1
    (20, 0, 6, 26),  # max: 20 + 6 - 0 = 26
], ids=["normal", "min_damage", "max_hit"])
def test_compute_damage(atk: int, def_: int, roll: int, expected: int) -> None:
    assert compute_damage(atk, def_, roll) == expected
```

Run it:

```
pytest test_combat.py -v
```

Expected output:

```
test_combat.py::test_compute_damage[normal] PASSED
test_combat.py::test_compute_damage[min_damage] PASSED
test_combat.py::test_compute_damage[max_hit] PASSED
```

---

## Add It to the Game

Open `test_combat.py`. Two TODOs wait for you:

**TODO 1** — Parametrize `compute_damage`:

```python
@pytest.mark.parametrize("atk,def_,roll,expected", [
    (10, 5, 3, 8),    # normal hit
    (5, 10, 1, 1),    # minimum — never 0
    (20, 0, 6, 26),   # maximum hit
], ids=["normal", "min_damage", "max_hit"])
def test_compute_damage_parametrized(atk: int, def_: int, roll: int, expected: int) -> None:
    assert compute_damage(atk, def_, roll) == expected
```

**TODO 2** — Parametrize `simulate_turn` to cover three outcomes: hero wins, hero loses, both survive.

Hint: control the outcome with specific stats.

- Hero wins if `hero.atk + hero_roll - monster.def_ >= monster.hp`
- Hero loses if `monster.atk + monster_roll - hero.def_ >= hero.hp` (and hero didn't kill the monster)
- Both survive otherwise

---

## Try It Yourself

1. Uncomment TODO 1. Run `pytest -v`. Verify three new test names appear with your `ids=`.
2. Write TODO 2 with at least three cases and `ids=`.
3. Run `uv run python check.py` to verify.

---

## Break It

Change one expected value in a parametrized case, e.g. `(10, 5, 3, 99)`. Run pytest. Notice the error message includes the case id — that's why `ids=` matters.

---

## Fix It

Restore the correct expected value. Re-run check.py.

---

## Side Quest: pytest-cases

[pytest-cases](https://smarie.github.io/python-pytest-cases/) extends parametrize with named case classes — useful when test inputs are complex objects rather than simple tuples. Not needed for this course, but worth knowing exists.

---

## Real-World Translation

| Game mechanic | Production use |
|---|---|
| `compute_damage` edge cases | Data transformation function with boundary inputs |
| `simulate_turn` outcomes | State machine transitions (win/lose/draw) |
| `ids=` readable names | CI failure logs that pinpoint the exact scenario |
| `xfail` known bug | Tracking a known regression without blocking CI |

---

## Checklist

- [ ] `@pytest.mark.parametrize` used at least twice in `test_combat.py`
- [ ] `ids=` used in at least one parametrize call
- [ ] Total test cases ≥ 8 (parametrize multiplies plain tests)
- [ ] `uv run python check.py` prints `✅ Mission 05 complete!`
