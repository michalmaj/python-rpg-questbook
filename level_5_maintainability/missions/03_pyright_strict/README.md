# Mission 03: pyright Strict Mode

## Goal

Add a `[tool.pyright]` section to `pyproject.toml` with `typeCheckingMode = "strict"` and fix any errors that pyright reports that mypy missed.

## Game Problem

Our RPG code now passes `mypy --strict` — every function is annotated. But mypy and pyright are two different type-checkers with different rule sets. Pyright (the engine behind VS Code's Python extension, Pylance) is stricter in several areas: it demands that every branch of a function provably returns a value, it narrows types more aggressively, and it catches some `Any` leaks that mypy lets through with `ignore_missing_imports`.

Consider `load_hero_classes()`:

```python
def load_hero_classes() -> dict[str, dict[str, int | str]]:
    try:
        with open(DATA_DIR / "hero_classes.json") as f:
            return json.load(f)   # returns Any
    except Exception:
        return {}
```

Mypy accepts `json.load(f)` even though it returns `Any`, because `Any` is compatible with everything. Pyright in strict mode flags the implicit `Any` as a potential type-safety hole — you're claiming to return `dict[str, dict[str, int | str]]` but the actual value is unverified. The fix is a `# type: ignore[no-any-return]` comment (or a runtime validation step). Running both checkers gives you broader coverage than either alone.

## Python Concept — pyright and type narrowing

### Why two type-checkers?

mypy and pyright share the same goal (catch type errors before runtime) but implement the type system independently. Using both is like having two code reviewers — one may catch what the other misses.

| Feature | mypy | pyright |
|---|---|---|
| Maintained by | python/mypy team | Microsoft |
| Used in | many CI pipelines | VS Code / Pylance |
| `Any` propagation | lenient | strict (in strict mode) |
| Type narrowing | good | excellent |
| Speed | slower | very fast |

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
import json
from pathlib import Path

# mypy accepts this; pyright strict may flag the Any return
def load_config() -> dict[str, int]:
    return json.loads(Path("config.json").read_text())  # type: ignore[no-any-return]
```

```bash
uv run python -m pyright minimal_example.py
# 0 errors, 0 warnings, 0 informations
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

3. Fix any errors pyright reports. Common fixes needed after mypy:

| Pyright error | Fix |
|---|---|
| `Type of "append" is partially unknown` | Annotate the empty list explicitly: `monsters: list[Monster] = []` |
| `Return type ... is partially unknown` | Annotate `json.load()` result: `raw: dict[str, list[object]] = json.load(f)` |
| `Return type, "dict[str, ...]", is not assignable to return type "Any"` | Add `# type: ignore[no-any-return]` to the `json.load()` call |
| `Expression of type "int \| str" cannot be assigned to "int"` | Add `int(d["hp"])` casts in `make_hero()` |

4. Re-run `uv run python check.py` until all checks pass.

## Try It Yourself

- Remove `# type: ignore[no-any-return]` from `load_hero_classes()` and run pyright. What error does it report? Put it back when done.
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
