# Level 5: Production Quality and Maintainability

**Prerequisite:** Level 4 complete.

**Central thesis:** Your tool works. Now can a new developer understand it, change it safely, and ship it with confidence?

## Starter: `starter_unqualified_rpg/`

A fully working RPG with all Level 4 concepts — but with 6 labeled quality smells:
no type annotations, no tests, bare excepts, no custom exceptions, no pre-commit, no CI.

> **Note:** This is a simplified, self-contained training version prepared for quality tooling exercises.
> It runs as `uv run python main.py` (single file), not as an installable package like the Level 4 boss fight.
> The goal here is practicing ruff, mypy, pytest, coverage, pre-commit, and CI — not re-implementing the package structure.

Run it first: `cd starter_unqualified_rpg && uv run python main.py new-game --name Ada --class warrior`

## Missions

| # | Mission | Skill |
|---|---------|-------|
| 01 | [ruff Linting](missions/01_ruff_linting/README.md) | Configure and fix ruff violations |
| 02 | [mypy Type Checking](missions/02_mypy_type_checking/README.md) | Add type annotations, mypy strict |
| 03 | [pyright Strict](missions/03_pyright_strict/README.md) | Configure pyright, compare with mypy |
| 04 | [pytest Fixtures](missions/04_pytest_fixtures/README.md) | Write fixtures, test pure functions |
| 05 | [pytest Parametrize](missions/05_pytest_parametrize/README.md) | Cover edge cases without copy-paste |
| 06 | [Coverage](missions/06_coverage/README.md) | Measure and improve test coverage |
| 07 | [Error Handling](missions/07_error_handling/README.md) | Custom exception hierarchy |
| 08 | [pre-commit](missions/08_pre_commit/README.md) | Local quality gate |
| 09 | [GitHub Actions CI](missions/09_github_actions_ci/README.md) | Remote CI pipeline |

## Projects

**Checkpoint:** [Project 01: Quality Gate Rescue](projects/01_quality_gate_rescue/README.md) — fix a broken codebase until ruff, mypy, and pyright all pass.

**Checkpoint:** [Project 02: Combat Regression Suite](projects/02_combat_regression_suite/README.md) — write a parametrized pytest suite that finds a hidden bug (then documents it with xfail).

**Boss Fight:** [Project 03: Full Release Pipeline](projects/03_full_release_pipeline/README.md) — start with the unqualified RPG and wire all 9 quality tools. Ship v1.0.0.

## How to start

```bash
uv run python tools/course_status.py   # see your progress
```
