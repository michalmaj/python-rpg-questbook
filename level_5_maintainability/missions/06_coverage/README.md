# Mission 06: Coverage

## Goal

Measure which lines and branches of `rpg.py` your tests actually exercise, find the one real gap the inherited test suite leaves open, and close it with a test that actually checks the result — not just one that runs the missing code.

---

## Game Problem

You have tests — but do they cover the corners? The goblin might die in the first hit, or survive and counterattack, or the hero's potions might already be empty. Without coverage measurement, you don't know which paths your tests never walk. Silent regressions hide in uncovered branches.

`pytest-cov` maps every line executed during your test run and tells you exactly what was missed.

### What coverage tells you — and what it doesn't

- **Line coverage** answers: was this line executed at all, by any test?
- **Branch coverage** answers a sharper question: for each `if`/`while`/etc., did a test take *both* outcomes — not just reach the line where the decision happens? A line can be "covered" by only ever taking one branch of it.
- **A high number can help you find gaps** — that's what this mission uses it for.
- **A high number does not prove your program is correct.** Coverage only tracks which code *ran*. A test with no assertion, or a wrong assertion, still counts as "covered" the moment the line executes:

  ```python
  def test_simulate_turn_both_survive(warrior, goblin):
      simulate_turn(warrior, goblin, hero_roll=1, monster_roll=1)
      # no assertion — this line is now "covered", but nothing was checked
  ```

  `check.py` in this mission specifically guards against that exact trap (see "Add It to the Game" below) — 100% coverage alone will not be enough.

Treat a coverage threshold as a guardrail that catches *obviously* untested code, not as a certificate of quality.

---

## Python Concept

### `pytest-cov` — coverage during test runs

Install once per project:

```bash
uv add --dev pytest-cov
```

Run with coverage:

```bash
uv run pytest --cov=rpg --cov-report=term-missing
```

Output adds a summary table:

```
Name     Stmts   Miss  Cover   Missing
--------------------------------------
rpg.py      42      6    86%   55, 78-82
```

The `Missing` column shows the exact line numbers not reached by any test.

### `--cov-report=html` — browsable report

```bash
uv run pytest --cov=rpg --cov-report=html
```

Opens `htmlcov/index.html` in a browser — green lines are covered, red are not.

### `--cov-fail-under=80` — enforce a threshold

```bash
uv run pytest --cov=rpg --cov-fail-under=80
```

Exits with a non-zero code if coverage drops below 80%. Useful in CI.

### `# pragma: no cover` — intentional exclusion

```python
def debug_dump(self) -> str:  # pragma: no cover
    """Development helper — not tested."""
    return repr(self)
```

Lines marked `# pragma: no cover` are excluded from the coverage count. Use sparingly — only for code that genuinely cannot or should not be tested (e.g., `if __name__ == "__main__":` blocks).

### `[tool.coverage.run]` vs `[tool.coverage.report]`

Configure coverage in `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["rpg"]        # which modules to measure
omit = ["test_*.py"]   # exclude test files themselves
branch = true           # track both outcomes of each decision, not just the line

[tool.coverage.report]
fail_under = 100        # minimum acceptable coverage for this mission
show_missing = true     # print missing line numbers in terminal
```

`[tool.coverage.run]` controls *what gets measured* — `branch = true` is what turns on branch coverage instead of plain line coverage.
`[tool.coverage.report]` controls *how results are displayed and enforced*.

Run with branch coverage on the command line too — this repo's pytest-cov does not reliably pick up `branch = true` from `pyproject.toml` alone:

```bash
uv run pytest --cov=rpg --cov-branch --cov-report=term-missing
```

---

## Minimal Example

```python
# rpg.py
def compute_damage(atk: int, def_: int, roll: int) -> int:
    return max(1, atk + roll - def_)

# test_combat.py
def test_compute_damage_normal() -> None:
    assert compute_damage(10, 5, 3) == 8

def test_compute_damage_minimum() -> None:
    assert compute_damage(5, 10, 1) == 1
```

```bash
uv run pytest --cov=rpg --cov-report=term-missing
```

```
Name     Stmts   Miss  Cover
----------------------------
rpg.py       2      0   100%
```

---

## Add It to the Game

The test suite you inherited from M04/M05 already covers 98% of `rpg.py` (97% of branches) before you write a single new line. There is exactly one real gap — this mission is about finding and closing that one gap properly, not about hitting a percentage.

### Step 1 — Add coverage config to `pyproject.toml`

Open `pyproject.toml`. Find the TODO comment and replace it with:

```toml
[tool.coverage.run]
source = ["rpg"]
omit = ["test_*.py"]
branch = true

[tool.coverage.report]
fail_under = 100
show_missing = true
```

### Step 2 — Run coverage and read the report

```bash
uv run pytest --cov=rpg --cov-branch --cov-report=term-missing
```

Look at the `Missing` column — it names the one line that's never reached: `simulate_turn`'s "both survive" outcome (`return True, True`), for a turn where neither the hero nor the monster dies.

### Step 3 — Write a test that actually checks it, not just runs it

```python
def test_simulate_turn_both_survive(warrior: Hero, goblin: Monster) -> None:
    hero_alive, monster_alive = simulate_turn(warrior, goblin, hero_roll=1, monster_roll=1)
    assert hero_alive is True
    assert monster_alive is True
```

`check.py` does not stop at "coverage reached 100%". It also swaps in a version of `simulate_turn` where the "both survive" outcome is reported backwards, and re-runs your suite — if your new test only *calls* `simulate_turn` without asserting on `hero_alive`/`monster_alive`, coverage will read 100% but this check still fails, because nothing would have noticed the bug.

---

## Try It Yourself

1. Add `[tool.coverage.run]` (with `branch = true`) and `[tool.coverage.report]` to `pyproject.toml`.
2. Run `uv run pytest --cov=rpg --cov-branch --cov-report=term-missing`.
3. Identify the missing line/branch.
4. Write a test that exercises it *and* asserts on what it returns.
5. Run `uv run python check.py` to verify.

---

## Break It

Remove the `branch = true` line from `[tool.coverage.run]` in `pyproject.toml`. Run `check.py`. You will see:

```
❌ [tool.coverage.run] must set branch = true
```

Restore the line and re-run.

---

## Fix It

Add `branch = true` back. Re-run `uv run python check.py`.

---

## Side Quest: Codecov Badge

1. Push your repo to GitHub.
2. Sign up at [codecov.io](https://codecov.io) and connect your repo.
3. Add this to your CI workflow:

```yaml
- name: Upload coverage
  uses: codecov/codecov-action@v4
```

4. Add the badge to your `README.md`:

```markdown
[![codecov](https://codecov.io/gh/yourname/yourrepo/branch/main/graph/badge.svg)](https://codecov.io/gh/yourname/yourrepo)
```

Now every PR shows a coverage delta — reviewers can see if new code is tested.

---

## Real-World Translation

| Game mechanic | Production use |
|---|---|
| `compute_damage` branch (minimum = 1) | Edge-case guard in a business rule |
| `simulate_turn` three outcomes | State machine with happy/sad/neutral paths |
| `# pragma: no cover` | CLI entry points, debug helpers |
| `fail_under = N` | CI gate that blocks merging undertested code — a guardrail, not a quality score |
| `htmlcov/` report | PR review tool: "which lines did you add but not test?" |

---

## Checklist

- [ ] `[tool.coverage.run]` section added to `pyproject.toml`, with `branch = true`
- [ ] `[tool.coverage.report]` section added to `pyproject.toml`, with `fail_under = 100`
- [ ] `uv run pytest --cov=rpg --cov-branch --cov-report=term-missing` runs without errors
- [ ] Branch coverage for `rpg.py` is 100%
- [ ] The new test asserts on `simulate_turn`'s actual return values for the "both survive" case — not just calling it
- [ ] `uv run python check.py` prints `✅ Mission 06 complete!`
