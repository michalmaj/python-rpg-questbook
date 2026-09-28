# Mission 03: pyright Strict Mode

## Goal

Add a `[tool.pyright]` section to `pyproject.toml` with `typeCheckingMode = "strict"`, then diagnose and fix the one real error pyright reports that mypy does not.

## Game Problem

Our RPG code now passes `mypy --strict` — every function is annotated. But mypy and pyright are two different type-checkers, built independently, with different rule sets. They overlap heavily (most real type errors trip both), but each has areas where it digs deeper than the other. Pyright's `reportUnknownMemberType` / `reportUnknownVariableType` checks are one of those areas: they track *inferred* types more aggressively than mypy's default strict mode does, including types inferred for local variables with no annotation at all.

Look at `load_monsters()` in `task.py`:

```python
def load_monsters() -> list[Monster]:
    try:
        with open(DATA_DIR / "monsters.json") as f:
            raw: dict[str, list[object]] = json.load(f)
        monsters = []  # TODO: pyright flags this — see Mission 03 README
        for entry in raw["monsters"]:
            try:
                monsters.append(MonsterConfig.model_validate(entry).to_domain())
            except Exception:
                pass
        return monsters
    except Exception:
        return []
```

`monsters = []` has no annotation, so its type is inferred purely from how it's used. mypy is satisfied — the function's declared return type is `list[Monster]`, and mypy trusts that declaration at the boundary. Pyright in strict mode is not satisfied: it tracks `monsters` as `list[Unknown]` at the point it's created, flags `.append()` on it as calling a method with an unknown parameter type, and flags the `return monsters` statement itself as returning a partially-unknown type — *before* it even gets to comparing that against the declared `-> list[Monster]`. Add the same annotation mypy implicitly assumed you meant, and both tools agree:

```python
monsters: list[Monster] = []
```

Verified directly against this repo's pinned versions (pyright 1.1.411, mypy 2.1.0): the unannotated version is 0 errors under `mypy --strict` and 2 errors under `pyright --strict`; annotating the variable brings pyright to 0 errors too, with no change to mypy's result either way.

## Python Concept — pyright and type narrowing

### Why two type-checkers?

mypy and pyright share the same goal (catch type errors before runtime) but implement the type system independently. They overlap on most real errors — a wrong argument type, a missing return, an incompatible assignment will usually trip both. Using both is still worth it: independent implementations occasionally disagree at the edges (like the unannotated-list case above), and each has its own home — mypy is the checker most CI pipelines default to; pyright is the engine behind VS Code's Python extension (Pylance), so it's the one giving you real-time feedback as you type.

| Feature | mypy | pyright |
|---|---|---|
| Maintained by | python/mypy team | Microsoft |
| Used in | many CI pipelines | VS Code / Pylance |
| Inferred-type strictness for unannotated locals | does not flag `x = []` on its own | flags it in strict mode (`reportUnknownVariableType`, `reportUnknownMemberType`) — see the `monsters` example above |

### Configuring pyright

Add to `pyproject.toml`:

```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
```

Run it:

```bash
uv run python -m pyright task.py
```

### Type narrowing

Pyright excels at narrowing union types inside conditionals:

```python
def load_hero() -> Hero | None:
    ...

hero = load_hero()
# hero is Hero | None here
if hero is None:
    return
# pyright narrows: hero is Hero here — no cast needed
hero.take_damage(10)   # safe
```

### `TypeGuard` — custom narrowing functions

When pyright cannot narrow automatically, you can write a `TypeGuard` function:

```python
from typing import TypeGuard

def is_hero(obj: object) -> TypeGuard[Hero]:
    return isinstance(obj, Hero)
```

Any `if is_hero(x):` block then treats `x` as `Hero` inside the branch.

## Minimal Example

```python
# mypy --strict: 0 errors. pyright --strict: 2 errors (reportUnknownMemberType,
# reportUnknownVariableType) — the unannotated local leaks an unknown type.
def build_list() -> list[int]:
    items = []
    items.append(1)
    return items
```

```bash
uv run python -m pyright minimal_example.py
# 2 errors, 0 warnings, 0 informations

# Fix: annotate the local explicitly.
#   items: list[int] = []
# Re-run — both mypy and pyright report 0 errors.
```

## Add to the Game

1. Open `pyproject.toml` and add the pyright section:

```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
```

2. Run pyright and review any errors:

```bash
uv run python -m pyright task.py
```

3. Fix the error pyright reports in `load_monsters()`:

| Pyright error | Fix |
|---|---|
| `Type of "append" is partially unknown` / `Return type, "list[Unknown]", is partially unknown` | Annotate the empty list explicitly: `monsters: list[Monster] = []` |

That is the one error this mission asks you to fix. (`make_hero()` already has its `int(d["hp"])` casts in place — those exist for the same reason: without them, `d["hp"]` has type `int | str`, which both mypy and pyright reject where a plain `int` is required.)

4. Re-run `uv run python check.py` until all checks pass.

## Try It Yourself

- Remove the annotation you just added from `monsters` (back to `monsters = []`) and re-run pyright. Confirm you get the same two errors back. Restore it when done.
- What happens if you change `typeCheckingMode = "strict"` to `typeCheckingMode = "basic"`? Does check.py still pass? (Hint: re-read the check logic.)
- Add `reveal_type(hero)` after the `if hero is None: return` guard in the `simulate` command. Run pyright and observe how it has narrowed `Hero | None` to `Hero`.

## Side Quest — basedpyright

[basedpyright](https://github.com/DetachHead/basedpyright) is a community fork of pyright with even stricter defaults and better error messages. Install it with:

```bash
uv add --dev basedpyright
uv run python -m basedpyright task.py
```

It uses the same `[tool.pyright]` configuration section, so no extra config is needed. Try it and compare its output to standard pyright.

## Checklist

- [ ] `pyproject.toml` has a `[tool.pyright]` section with `typeCheckingMode = "strict"`
- [ ] `uv run python -m pyright task.py` exits with 0 errors
- [ ] `uv run mypy task.py --strict` still exits with code 0 (no regression)
- [ ] `uv run python check.py` prints "Mission 03 complete!"
