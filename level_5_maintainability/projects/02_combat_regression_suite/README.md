# Project 02: Combat Regression Suite

**Requires:** Level 5, Missions 04–06 (pytest Fixtures, pytest Parametrize, Coverage)

## What you will do

The `rpg/combat.py` module is a working combat engine — with one hidden bug. Your job is to write a thorough pytest test suite that:

1. Covers normal behavior with fixtures and parametrize
2. **Finds the bug** in `compute_damage()`
3. Documents it with `@pytest.mark.xfail` so the suite still passes

**Do not fix the bug.** The lesson is: tests reveal bugs; xfail documents known issues.

## Structure

```
02_combat_regression_suite/
├── README.md               ← this file
├── check.py                ← run to verify
├── rpg/
│   ├── __init__.py
│   └── combat.py           ← production code — do NOT modify
└── tests/
    ├── __init__.py
    └── test_combat.py      ← write your tests here
```

## How to check

```bash
cd level_5_maintainability/projects/02_combat_regression_suite
uv run python check.py
```

## Requirements

| Requirement | Why |
|---|---|
| `pytest tests/test_combat.py` exits 0 | All tests pass (xfail counts as pass) |
| Coverage ≥85% on `rpg/combat.py` | You've tested the real behaviour, not just the happy path |
| ≥1 `@pytest.mark.parametrize` use | Cover multiple cases without copy-paste |
| ≥1 `@pytest.fixture` definition | Reusable test state |
| ≥1 `@pytest.mark.xfail(strict=True)` calling `compute_damage()` | Documents the known bug; fails if bug is silently fixed |

## The hidden bug

```python
compute_damage(atk=1, bonus=0, def_=10)
# returns 0 — but should return 1 (minimum damage is always 1)
```

Normal combat (atk > def_) works correctly. Only extreme edge cases expose the bug.

## xfail pattern

```python
@pytest.mark.xfail(strict=True, reason="known bug: minimum damage should be 1, not 0")
def test_minimum_damage_is_one():
    assert compute_damage(1, 0, 10) == 1  # currently returns 0
```

With `xfail`, pytest reports this as `XFAIL` — not a failure. The suite exits 0.
`strict=True` means: if the bug is accidentally fixed, pytest fails loudly (XPASS → error).

## Fixtures and parametrize hints

```python
@pytest.fixture
def goblin() -> Fighter:
    return Fighter(name="Goblin", hp=30, atk=8, def_=2)

@pytest.mark.parametrize("atk, bonus, def_, expected", [
    (10, 0,  3, 7),   # normal hit
    (10, 5,  3, 12),  # bonus attack
    (3,  0, 10, 0),   # attacker too weak (bug territory)
])
def test_compute_damage(atk, bonus, def_, expected):
    assert compute_damage(atk, bonus, def_) == expected
```

---

**Next:** [Project 03 — Full Release Pipeline (Boss Fight)](../03_full_release_pipeline/README.md)
