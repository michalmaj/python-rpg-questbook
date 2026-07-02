# Mission 09: GitHub Actions CI

## Goal

Create a `.github/workflows/ci.yml` file that runs ruff, mypy, and pytest
automatically on every push and pull request — on Python 3.12 and 3.13.

---

## Game Problem

You have pre-commit hooks from M08 that protect your local commits. But what
about your teammates? What about the pull request someone opens from a fork?
Pre-commit only runs on machines where it has been installed. A contributor
who skips `pre-commit install` can still push broken code.

GitHub Actions solves this. Every push triggers a workflow that runs ruff →
mypy → pytest on a clean Ubuntu machine. If any step fails, the PR is blocked.
The green checkmark next to a commit tells the whole team: *this code passed
quality checks on a machine that has no history with this developer.*

---

## Python Concept

### `.github/workflows/ci.yml`

GitHub Actions workflows are YAML files inside `.github/workflows/`. GitHub
reads them automatically — no registration needed.

```yaml
name: CI
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: uv sync
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run mypy . --strict
      - run: uv run pytest --cov=rpg --cov-report=xml -q
```

Key fields:

| Field | Meaning |
|---|---|
| `on:` | Events that trigger the workflow (`push`, `pull_request`) |
| `jobs:` | Top-level grouping of parallel or sequential job sets |
| `runs-on:` | The OS for the runner (`ubuntu-latest` is the standard) |
| `strategy.matrix` | Run the job once per item — here, two Python versions |
| `steps:` | Ordered list of actions and shell commands |
| `uses:` | Reference to a reusable Action from GitHub Marketplace |
| `run:` | A shell command to execute on the runner |

### `astral-sh/setup-uv`

The `setup-uv` action installs uv on the runner and sets the Python version
from the matrix. After it runs, `uv sync` installs your project's dependencies
from `pyproject.toml` and `uv.lock`.

### Why ruff before mypy before pytest?

Fast checks first. Ruff runs in milliseconds and catches style errors that
would cause mypy or pytest to produce confusing output. Mypy catches type
errors that could cause test failures. Pytest is last because it is the
slowest. This ordering gives the fastest feedback on the most common failures.

### Why a matrix with 3.12 and 3.13?

Your code must work on the Python versions your users have. A matrix multiplies
your job across every listed version. If 3.13 introduces a breaking change,
the matrix catches it before it reaches your users.

---

## Minimal Example

The complete CI workflow to create at
`.github/workflows/ci.yml` inside this mission folder:

```yaml
name: CI
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: uv sync
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run mypy . --strict
      - run: uv run pytest --cov=rpg --cov-report=xml -q
```

---

## Add It to the Game

### Step 1 — Create the directory structure

Inside this mission folder:

```bash
mkdir -p .github/workflows
```

### Step 2 — Create `ci.yml`

Create `.github/workflows/ci.yml` with the full workflow above.

Make sure your file includes:

- `on:` at the top level with `push` and `pull_request` triggers
- `jobs:` section with at least one job
- `uv` setup step (using `astral-sh/setup-uv`)
- `ruff` check step
- `mypy` step
- `pytest` step
- A matrix with `"3.12"` and `"3.13"`

Steps must be ordered: ruff before mypy, mypy before pytest.

### Step 3 — Verify locally

```bash
uv run python check.py
```

`check.py` verifies the YAML structure and confirms that ruff and mypy pass
on `task.py`. It cannot actually run the GitHub Actions workflow — that
requires a push to GitHub.

### Step 4 — Push to GitHub and see it run

To see the workflow execute for real, copy your `ci.yml` to your own repo's
`.github/workflows/` folder and push. Open the Actions tab on GitHub to watch
each step run. When all steps pass, a green checkmark appears next to the
commit.

> **Note:** `check.py` verifies your YAML structure locally. The real CI
> experience requires pushing to a GitHub repository with Actions enabled.

---

## Try It Yourself

1. Create the directory: `mkdir -p .github/workflows`
2. Create `.github/workflows/ci.yml` with the workflow above
3. Make sure all required keywords are present: `on:`, `jobs:`, `uv`, `ruff`,
   `mypy`, `pytest`, `3.12`, `3.13`
4. Make sure steps are ordered: ruff → mypy → pytest
5. Run `uv run python check.py`

---

## Break It

Change the order of steps so that pytest comes before mypy:

```yaml
      - run: uv run pytest --cov=rpg --cov-report=xml -q
      - run: uv run mypy . --strict
```

Run `uv run python check.py`. You will see:

```
❌ Steps should be ordered: ruff → mypy → pytest (fast checks first)
```

Restore the correct order and run `check.py` again.

---

## Fix It

Revert the step order. Run `uv run python check.py`. All checks should pass.

---

## Side Quest: Coverage Artifact and Codecov

The pytest step in the YAML uses `--cov-report=xml` to produce a
`coverage.xml` file. Upload it to [Codecov](https://codecov.io) to get a
coverage badge in your README:

```yaml
      - uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
```

Add this step after pytest. Codecov is free for open-source projects and
shows you which lines are not covered by tests — displayed as a PR comment
on every pull request.

---

## Real-World Translation

| Game mechanic | Production use |
|---|---|
| `.github/workflows/ci.yml` | Automated quality gate on every PR |
| `on: [push, pull_request]` | Triggers on all code changes, not just merges |
| `strategy.matrix` | Tests multiple Python versions in parallel |
| `astral-sh/setup-uv` | Fast, reproducible dependency install in CI |
| `ruff → mypy → pytest` | Fast checks first, slow checks last |
| Green checkmark on commit | Signal to reviewers that code quality passed |

---

## Checklist

- [ ] `.github/workflows/ci.yml` exists inside this mission folder
- [ ] `on:` trigger is present with `push` and/or `pull_request`
- [ ] `jobs:` section is present
- [ ] `uv` appears in a setup step
- [ ] `ruff` step is present and comes before `mypy`
- [ ] `mypy` step is present and comes before `pytest`
- [ ] `pytest` step is present
- [ ] Matrix includes `"3.12"` and `"3.13"`
- [ ] `uv run python check.py` prints `✅ Mission 09 complete!`
