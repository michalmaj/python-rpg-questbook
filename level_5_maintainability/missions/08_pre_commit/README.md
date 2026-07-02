# Mission 08: Pre-commit Hooks

## Goal

Wire up pre-commit hooks for ruff and mypy so that every commit is automatically
checked for style errors and type errors — before the bad code ever reaches `main`.

---

## Game Problem

You have a clean, fully-typed RPG in `task.py`. The linting and type-checking
you learned in M01–M03 works perfectly when you remember to run it. But when
you are deep in a dungeon feature and just want to commit, you forget. The
linter finds six style violations. Mypy flags a missing return type. The code
reaches `main` and CI fails — everyone is blocked.

Pre-commit hooks run automatically on every `git commit`. They catch the same
ruff and mypy errors you already know how to fix, but they do it for you,
every time, before the commit lands. A bad commit cannot reach `main` because
it never finishes.

---

## Python Concept

### `.pre-commit-config.yaml`

Pre-commit is configured by a `.pre-commit-config.yaml` file. Each entry in
`repos:` points to a GitHub repository that provides one or more hooks.

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.13
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.16.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic
          - typer
          - rich
```

Key fields:

| Field | Meaning |
|---|---|
| `repo:` | GitHub URL of the hook provider |
| `rev:` | Pinned version tag — never use `latest` |
| `id:` | Which hook from that repo to run |
| `args:` | Extra CLI arguments passed to the hook |
| `additional_dependencies:` | Extra packages the hook needs (e.g. mypy stubs) |

### Hook lifecycle

1. `pre-commit install` — registers the hook in `.git/hooks/pre-commit`
2. On every `git commit`, the hook runner checks out the staged files into a
   temporary environment and runs each configured hook.
3. If any hook exits non-zero, the commit is aborted. Fix the errors, re-stage,
   and commit again.
4. `pre-commit run --all-files` — runs all hooks on every file right now,
   without needing to stage anything.

### Why pin `rev:`?

Unpinned hooks silently upgrade when the upstream repo tags a new version.
A new mypy version may flag errors that the old version did not. Pinning
`rev:` keeps the team on the same version until you explicitly decide to
upgrade.

---

## Minimal Example

Create `.pre-commit-config.yaml` in this folder:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.13
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.16.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic
          - typer
          - rich
```

Then verify it passes against `task.py`:

```bash
pre-commit run --all-files --config .pre-commit-config.yaml
```

---

## Add It to the Game

### Step 1 — Install pre-commit

Pre-commit is a standalone tool. Install it once:

```bash
uv tool install pre-commit
```

Verify it is available:

```bash
pre-commit --version
```

### Step 2 — Create `.pre-commit-config.yaml`

Create `.pre-commit-config.yaml` in this mission folder
(`level_5_maintainability/missions/08_pre_commit/`) with at minimum:

- A ruff hook (`id: ruff`) from `ruff-pre-commit`
- A ruff-format hook (`id: ruff-format`) from `ruff-pre-commit`
- A mypy hook (`id: mypy`) from `mirrors-mypy`
- Pinned `rev:` for every repo

Add `additional_dependencies` under mypy for any third-party packages that
`task.py` imports: `pydantic`, `typer`, `rich`.

### Step 3 — Run against task.py

```bash
pre-commit run --all-files --config .pre-commit-config.yaml
```

All hooks should pass. If mypy fails, check the `additional_dependencies` list.

### Step 4 — Run check.py

```bash
uv run python check.py
```

---

## Try It Yourself

1. Install pre-commit: `uv tool install pre-commit`
2. Create `.pre-commit-config.yaml` in this folder with ruff + ruff-format + mypy hooks
3. Pin each hook to a specific `rev:` tag
4. Run `pre-commit run --all-files --config .pre-commit-config.yaml` — all hooks must pass
5. Run `uv run python check.py`

---

## Break It

Introduce a type error into a copy of `task.py`:

```python
def compute_damage(atk: int, def_: int, roll: int) -> str:  # wrong return type
    return max(1, atk + roll - def_)
```

Run pre-commit again:

```bash
pre-commit run --all-files --config .pre-commit-config.yaml
```

Mypy will catch the return type mismatch immediately. Revert the change and
confirm the hook passes again.

---

## Fix It

Revert the type error. Re-run pre-commit. All hooks should be green.

---

## Side Quest: Commitizen for Conventional Commits

[Commitizen](https://commitizen-tools.github.io/commitizen/) enforces
[Conventional Commits](https://www.conventionalcommits.org/) format:
`feat: add hero status command`, `fix: prevent negative HP`, etc.

Add it as a pre-commit hook:

```yaml
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v4.8.3
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

The `stages: [commit-msg]` means it runs on the commit message, not on the
files. Commitizen will reject commits that do not follow the conventional
format. This keeps your `git log` readable and enables automatic changelog
generation.

---

## Real-World Translation

| Game mechanic | Production use |
|---|---|
| `.pre-commit-config.yaml` | Shared hook config committed to every repo |
| `ruff` hook | Enforces style rules on every contributor's machine |
| `mypy` hook | Catches type errors before they reach CI |
| `rev:` pinning | Reproducible hook versions across the team |
| `pre-commit install` | Run once per developer after cloning the repo |
| `pre-commit run --all-files` | Run in CI to verify all files pass hooks |

---

## Checklist

- [ ] `pre-commit` is installed (`uv tool install pre-commit`)
- [ ] `.pre-commit-config.yaml` exists in this mission folder
- [ ] `repos:` key present at the top level
- [ ] `ruff` hook from `ruff-pre-commit` included
- [ ] `ruff-format` hook from `ruff-pre-commit` included
- [ ] `mypy` hook from `mirrors-mypy` included
- [ ] Every repo has a pinned `rev:` tag
- [ ] `pre-commit run --all-files` passes against `task.py`
- [ ] `uv run python check.py` prints `✅ Mission 08 complete!`
