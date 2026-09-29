# Boss Fight: Full Release Pipeline

## You Have Earned This

You survived nine missions of pain: linting, type checking, testing, coverage, error
handling, pre-commit hooks, and CI. You know what each tool does and why it matters.

Now you wire them all together in one project — from a messy, untested codebase to a
fully qualified release with a `v1.0.0` tag and a green CI badge.

This is what shipping production Python looks like.

---

## What You're Building

A **full release pipeline** for an RPG game:

| Layer | Tool | What it catches |
|-------|------|-----------------|
| Style + lint | ruff | import order, dead code, old syntax |
| Type safety | mypy --strict | missing annotations, wrong types |
| Type inference | pyright | additional static analysis |
| Unit tests | pytest | logic regressions |
| Coverage | pytest-cov | untested code paths |
| Git hooks | pre-commit | bad commits never happen |
| Continuous Integration | GitHub Actions | bad merges never happen |
| Changelog | CHANGELOG.md | every release is documented |

---

## Starting Point

`rpg.py` is your hero — but it has **6 quality smells** baked in:

- **Smell 1** — Ruff violations: mixed imports on one line, unused import, old `Optional`/`List` syntax
- **Smell 2** — Missing type annotations on methods and functions
- **Smell 3** — No pyright config, so hidden type errors go undetected
- **Smell 4** — No tests at all — a one-line change can silently break everything
- **Smell 5** — Bare `except:` swallows every error without a trace
- **Smell 6** — No pre-commit hooks, no CI — broken code can reach `main` unchecked

Your job: fix all six smells and wire up the full pipeline.

---

## Checklist (9 tasks, one per quality layer)

Work through these in order. Run `uv run python check.py` after each step.

- [ ] **1. pyproject.toml** — create it with `[tool.ruff]`, `[tool.mypy]`,
  `[tool.pyright]`, `[tool.coverage]`, and `[tool.pytest.ini_options]` sections.
  Configure ruff to select `E`, `F`, `W`, `I`, `UP`. Set mypy to strict mode.
  Set coverage minimum to 80%.

- [ ] **2. Fix rpg.py — ruff** — run `uv run ruff check rpg.py` and fix every
  violation. Split the mixed import line, remove the unused `csv` import, replace
  `Optional[X]` / `List[X]` with `X | None` / `list[X]`, and break any lines over
  the configured line length.

- [ ] **3. Fix rpg.py — mypy** — run `uv run mypy rpg.py --strict` and add all
  missing type annotations. Every method, property, and function needs a return type.
  Every parameter needs a type. Replace bare `except:` with typed `except Exception:`.

- [ ] **4. Write tests** — create `tests/conftest.py` and `tests/test_combat.py`.
  Test `compute_damage`, `Hero.take_damage`, `Hero.use_potion`, `Monster.take_damage`,
  `simulate_one`, and `make_hero`. Aim for ≥ 80% coverage on `rpg.py`.

- [ ] **5. Coverage** — run `uv run pytest --cov=rpg --cov-report=term-missing` and
  confirm `rpg.py` hits 80%+. Add more tests if needed.

- [ ] **6. CHANGELOG.md** — create it following the Keep a Changelog format. Add a
  `## [1.0.0]` section with bullet points for what this release includes.

- [ ] **7. pre-commit** — create `.pre-commit-config.yaml` with ruff, ruff-format,
  and mypy hooks. Run `uv run pre-commit install` then
  `uv run pre-commit run --files rpg.py --config .pre-commit-config.yaml`.
  Use `--files`, not `--all-files`: this repo is a multi-level monorepo, and
  `--all-files` runs on every file git tracks across every level, not just
  this project — see Mission 08 for why that matters.

- [ ] **8. GitHub Actions** — create `.github/workflows/ci.yml`. It must install uv,
  run ruff, mypy, and pytest on both Python 3.12 and 3.13 in a matrix.

- [ ] **9. Final check** — run `uv run python check.py`. All 7 steps must pass.

---

## Final Step

When `check.py` shows all green:

```bash
git add .
git commit -m "feat: complete full release pipeline"
git push origin your-branch
```

Open a pull request. Watch the CI badge turn green. Then tag your release:

```bash
git tag v1.0.0
git push origin v1.0.0
```

You have shipped a production-quality Python project.

---

## Running check.py

```bash
uv run python check.py
```

Expected output when everything is complete:

```
Checking boss fight: full_release_pipeline
==================================================
✓ pyproject.toml has all required tool sections
✓ .pre-commit-config.yaml has ruff, ruff-format, mypy hooks
✓ .github/workflows/ci.yml has ruff, mypy, pytest, uv, matrix [3.12, 3.13]
✓ CHANGELOG.md has 1.0.0 section
✓ ruff check passes
✓ mypy --strict passes
✓ All tests pass
✓ Coverage for rpg.py: 85%

✅ Boss fight complete!
   Your project has: ruff ✓  mypy ✓  pyright config ✓
   pre-commit ✓  CI ✓  tests ✓  coverage ✓  CHANGELOG ✓

   Final step: push your branch, open a PR, and confirm the CI badge goes green.
   Then create a git tag: git tag v1.0.0 && git push origin v1.0.0
```
