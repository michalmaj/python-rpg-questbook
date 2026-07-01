# Mission 01: Ruff Linting

## Goal

Configure ruff in a local `pyproject.toml` and fix all lint and style violations in `task.py`.

## Game Problem

The RPG codebase works — monsters are defeated, saves are persisted, reports are generated — but the code quality layer is missing. Import statements are tangled, old typing syntax lingers, lines run far past the screen edge, and bare `except:` blocks silently swallow errors. When another developer (or future you) opens this file, it is hard to read and easy to break. Ruff is the automated quality guard that catches these issues before they spread.

## Python Concept — ruff rule categories

Ruff is a fast Python linter and formatter. Rules are grouped into categories:

| Category | Prefix | What it catches |
|----------|--------|-----------------|
| pycodestyle | `E` / `W` | PEP 8 style: whitespace, blank lines, line length |
| Pyflakes | `F` | Unused imports, undefined names |
| isort | `I` | Import order |
| pyupgrade | `UP` | Outdated syntax (`Optional[X]` → `X \| None`, `List` → `list`) |
| flake8-bugbear | `B` | Common bugs and design issues |

## Minimal Example

```toml
# pyproject.toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
```

```bash
uv run ruff check task.py        # show violations
uv run ruff check --fix task.py  # auto-fix what ruff can
uv run ruff format task.py       # apply formatter
```

## Add to the Game (fix task.py)

1. Open `pyproject.toml` and replace `select = []` with `select = ["E", "F", "I", "UP", "B"]`.
2. Run `uv run ruff check task.py` to see all violations listed.
3. Run `uv run ruff check --fix task.py` to auto-fix what ruff can.
4. Manually fix remaining issues (bare `except:` → `except Exception:`, long lines, unused imports).
5. Run `uv run ruff format task.py` to apply the formatter.
6. Run `uv run python check.py` to confirm all checks pass.

## Try It Yourself

- Which violations did ruff fix automatically and which required manual edits?
- Add rule `"N"` (pep8-naming) to `select` — what new violations appear?
- Try `--select E501` to check only line-length violations.

## Side Quest — `ruff check --select ALL`

Run:

```bash
uv run ruff check --select ALL task.py
```

This enables every rule ruff knows. How many violations appear? Which categories produce the most noise on this file? Are any of them genuinely useful warnings, or just style preferences?

## Checklist

- [ ] `pyproject.toml` has `[tool.ruff.lint]` with a non-empty `select`
- [ ] `uv run ruff check task.py` exits with code 0 (no violations)
- [ ] `uv run ruff format --check task.py` exits with code 0 (formatted)
- [ ] No bare `except:` in `task.py`
- [ ] No deprecated typing syntax (`Optional[`, `List[` from `typing`)
- [ ] `uv run python check.py` prints "Mission 01 complete!"
