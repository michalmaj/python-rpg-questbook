# Mission 04: pytest Fixtures

## Goal

Write `conftest.py` with three fixtures and `test_combat.py` with six tests for the pure RPG domain functions in `rpg.py`.

---

## Game Problem

You refactor the damage formula — `compute_damage` — to fix a balance issue. The game still runs. Combat still happens. Monsters still die.

Three sessions later you notice heroes are dying too easily. Something broke. You have no idea when.

Automated tests would have caught it immediately. But right now you have none.

---

## Python Concept: pytest Fixtures

A **fixture** is a function that provides test data. pytest injects it into test functions by matching parameter names.

### conftest.py

Fixtures defined in `conftest.py` are automatically available to every test file in the same directory — no import needed.

```python
# conftest.py
import pytest

@pytest.fixture
def warrior():
    return Hero(name="Ada", hp=120, ...)
```

```python
# test_combat.py
def test_hero_takes_damage(warrior):  # pytest injects warrior automatically
    warrior.take_damage(10)
    assert warrior.hp == 110
```

### Fixture scope

By default, fixtures run once per test function. Each test gets a fresh object.

```python
@pytest.fixture(scope="session")  # runs once for the whole test session
def db_connection(): ...
```

### Factory fixture

When you need customized objects, return a factory function from the fixture:

```python
@pytest.fixture
def make_hero():
    def _make(**kwargs) -> Hero:
        defaults = dict(name="TestHero", hp=120, ...)
        return Hero(**{**defaults, **kwargs})
    return _make

# In a test:
def test_no_potions(make_hero):
    hero = make_hero(potions=0)
    assert hero.use_potion() is False
```

---

## Minimal Example

```python
# conftest.py
import pytest

@pytest.fixture
def gold_amount() -> int:
    return 100

# test_gold.py
def test_gold_positive(gold_amount):
    assert gold_amount > 0
```

Run with:
```bash
pytest -v
```

---

## Add It to the Game

You have three files to work with:

- `rpg.py` — pure domain functions, **do not edit**
- `conftest.py` — fill in the three fixture TODOs
- `test_combat.py` — fill in the six test TODOs

### Step 1: Fill in `conftest.py`

Uncomment and complete each `@pytest.fixture` block:

1. `warrior` — returns a warrior `Hero` with the given stats
2. `goblin` — returns a `Monster` with the given stats
3. `make_hero` — returns a factory function for custom heroes

### Step 2: Fill in `test_combat.py`

Uncomment and complete each test function:

1. `test_compute_damage_normal_hit` — `compute_damage(10, 5, 3)` should return `8`
2. `test_compute_damage_minimum` — `compute_damage(5, 10, 1)` should return `1`
3. `test_hero_take_damage` — use the `warrior` fixture, deal damage, check `hp`
4. `test_use_potion_heals` — use the `warrior` fixture, use a potion, check `hp` increased
5. `test_use_potion_empty` — use `make_hero(potions=0)`, verify `use_potion()` returns `False`
6. `test_simulate_turn_hero_wins` — use `warrior` and a monster with `hp=1`, verify monster dies

### Step 3: Run the checker

```bash
python check.py
```

---

## Try It Yourself

Run `pytest -v` directly to see the test output:

```bash
pytest test_combat.py -v
```

Run a single test:

```bash
pytest test_combat.py::test_compute_damage_normal_hit -v
```

---

## Break It

Change `compute_damage` in `rpg.py` to return `atk - def_ + roll` (removing the `max(1, ...)`). Run tests. Which ones fail?

Then restore the original formula. Your tests caught the regression.

---

## Fix It

If a test fails with `AssertionError`, read the error message carefully. pytest shows you the actual vs expected values. Fix the assertion or the fixture, not `rpg.py` (which is already correct).

---

## Side Quest: monkeypatch

`simulate_turn` uses explicit roll parameters, so it's already deterministic in tests. But what if your code called `random.randint` directly?

```python
# If rpg.py used random internally:
def test_combat_always_hits(monkeypatch):
    monkeypatch.setattr("rpg.random.randint", lambda a, b: b)  # always max roll
    ...
```

`monkeypatch` is a built-in pytest fixture. No import needed — just add it as a parameter.

---

## Real-World Translation

| Game concept | Real-world equivalent |
|---|---|
| `warrior` fixture | A test database with seeded user accounts |
| `goblin` fixture | A mock HTTP response from an external API |
| `make_hero` factory | A builder for complex order objects in an e-commerce test suite |
| `conftest.py` | Shared test infrastructure for an entire Python package |

---

## Checklist

- [ ] `conftest.py` has `@pytest.fixture` for `warrior`, `goblin`, and `make_hero`
- [ ] `test_combat.py` has at least 5 `def test_` functions (all uncommented)
- [ ] All tests pass: `pytest -v`
- [ ] `python check.py` prints `✅ Mission 04 complete!`
