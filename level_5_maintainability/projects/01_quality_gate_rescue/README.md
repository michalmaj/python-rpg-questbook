# Project 01: Quality Gate Rescue

**Requires:** Level 5, Missions 01–03 (ruff Linting, mypy Type Checking, pyright Strict)

## What you will do

The `rpg/` package in this folder has intentional quality problems. Your job is to fix all of them until three quality gates pass with exit code 0:

```bash
ruff check rpg/      # no style violations
mypy --strict rpg/   # no type errors
pyright rpg/         # no type errors
```

Then write `QUALITY_REPORT.md` describing what each tool found.

## Structure

```
01_quality_gate_rescue/
├── README.md           ← this file
├── check.py            ← run to verify all gates pass
├── ruff.toml           ← ruff configuration (don't change this)
├── mypy.ini            ← mypy configuration (don't change this)
├── pyrightconfig.json  ← pyright configuration (don't change this)
├── QUALITY_REPORT.md   ← you create this
└── rpg/
    ├── __init__.py
    ├── domain.py       ← fix this file
    └── combat.py       ← fix this file
```

## How to check

Run all commands from the **repo root**:

```bash
uv run python level_5_maintainability/projects/01_quality_gate_rescue/check.py
```

## What is broken

Open `rpg/domain.py` and `rpg/combat.py`. You will find:

| Problem | Tool that catches it |
|---|---|
| Unused `import os` | ruff (F401) |
| `List[str]`, `Optional[int]`, `Dict[str, Any]` from `typing` | ruff (UP035), mypy |
| Missing return type annotations | mypy `--strict`, pyright |
| `Any` used where a concrete type is possible | mypy `--strict`, pyright |
| Line longer than 88 characters | ruff (E501) |

## Approach

Work tool by tool:

1. Fix ruff violations first — from the project dir: `uv run ruff check rpg/ --fix` catches some automatically
2. Add missing return type annotations (mypy will tell you exactly where)
3. Replace `Any` with concrete types (`Hero | Monster`, `list[Hero | Monster]`, etc.)
4. Run pyright last — it sometimes catches things mypy misses

## QUALITY_REPORT.md format

Write at least three sections:

```markdown
## ruff
What ruff found and how you fixed it.

## mypy
What mypy --strict found and how you fixed it.

## pyright
What pyright found (same as mypy? different? why?).
```

---

**Next:** [Project 02 — Combat Regression Suite](../02_combat_regression_suite/README.md)
