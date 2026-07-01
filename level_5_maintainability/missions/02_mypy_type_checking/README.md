# Mission 02: mypy Type Checking

## Goal

Add type annotations to every function and method in `task.py`, configure mypy strict mode, and make `uv run mypy task.py --strict` exit with zero errors.

## Game Problem

Look at this function signature:

```python
def compute_damage(atk, def_, roll):
    return max(1, atk + roll - def_)
```

What types are `atk`, `def_`, and `roll`? Integers? Floats? Can they be `None`? Without annotations, Python cannot answer that question — and neither can your editor. A caller could pass a string and the bug would only surface at runtime, mid-battle. The same problem exists across the entire RPG: `save_hero(hero)`, `make_hero(name, hero_class)`, `load_hero()` — none of them declare what they accept or return. mypy is the static type-checker that reads your annotations and catches type mismatches before the game even starts.

## Python Concept — type annotations

Python annotations describe the expected type of each parameter and the return value. They are checked by mypy at development time, not at runtime.

### Basic syntax

```python
def compute_damage(atk: int, def_: int, roll: int) -> int:
    return max(1, atk + roll - def_)
```

### Optional / union types (Python 3.10+ syntax)

```python
def load_hero() -> Hero | None:   # returns a Hero or nothing
    ...
```

### Container types

```python
def load_monsters() -> list[Monster]:       # a list of Monster objects
def load_hero_classes() -> dict[str, dict[str, int | str]]:
    ...
```

### `reveal_type()` — instant annotation helper

Insert `reveal_type(x)` anywhere in your code and run mypy. mypy prints the inferred type of `x` and then removes the call automatically.

```python
monsters = load_monsters()
reveal_type(monsters)  # mypy: Revealed type is "list[task.Monster]"
```

Delete the `reveal_type()` call once you know the type.

## Minimal Example

```python
from dataclasses import dataclass

@dataclass
class Spell:
    name: str
    damage: int

def cast(spell: Spell, target_def: int) -> int:
    return max(1, spell.damage - target_def)

hero_hp: int = 100
result: int = cast(Spell("Fireball", 30), 5)
```

```bash
uv run mypy minimal_example.py --strict
# Success: no issues found in 1 source file
```

## Add to the Game (annotate task.py)

1. Open `pyproject.toml` and add the mypy section at the end:

```toml
[tool.mypy]
strict = true
```

2. Run mypy to see all missing annotations:

```bash
uv run mypy task.py --strict
```

3. Add type annotations to every function signature listed below. Use the comments in `task.py` as a guide:

| Function / method | Expected annotation |
|---|---|
| `compute_damage(atk, def_, roll)` | `(atk: int, def_: int, roll: int) -> int` |
| `load_monsters()` | `-> list[Monster]` |
| `load_hero_classes()` | `-> dict[str, dict[str, int \| str]]` |
| `save_hero(hero)` | `(hero: Hero) -> None` |
| `load_hero()` | `-> Hero \| None` |
| `make_hero(name, hero_class)` | `(name: str, hero_class: HeroClass) -> Hero` |
| `simulate_one(hero, monster)` | `(hero: Hero, monster: Monster) -> bool` |
| `generate_reports(session)` | `(session: SessionSummary) -> tuple[Path, Path]` |
| `Hero.is_alive` (property) | `-> bool` |
| `Hero.take_damage(self, amount)` | `(self, amount: int) -> None` |
| `Hero.use_potion(self)` | `-> bool` |
| `Monster.is_alive` (property) | `-> bool` |
| `Monster.take_damage(self, amount)` | `(self, amount: int) -> None` |

4. Re-run mypy after each function until all errors are resolved.
5. Run `uv run python check.py` to confirm all checks pass.

## Try It Yourself

- Use `reveal_type()` on the return value of `load_monsters()` — what type does mypy infer before you annotate it?
- What happens if you annotate `compute_damage` to return `float` instead of `int`? Does mypy catch the mismatch where it is called?
- Remove `-> None` from `take_damage` and re-run mypy. Does the error message explain clearly what is missing?

## Side Quest — Google-style docstrings

Once your annotations are in place, add a Google-style docstring to `compute_damage`:

```python
def compute_damage(atk: int, def_: int, roll: int) -> int:
    """Calculate damage dealt after defense reduction.

    Args:
        atk: Attacker's base attack value.
        def_: Defender's defense value.
        roll: Dice roll result (1–6).

    Returns:
        Net damage, minimum 1.
    """
    return max(1, atk + roll - def_)
```

Add similar docstrings to `simulate_one` and `generate_reports`. Good docstrings and good type annotations work together: annotations tell the type, docstrings explain the intent.

## Checklist

- [ ] `pyproject.toml` has a `[tool.mypy]` section with `strict = true`
- [ ] `uv run mypy task.py --strict` exits with code 0
- [ ] `uv run ruff check task.py` still exits with code 0 (no regression)
- [ ] At least 8 function/method signatures have `->` return type annotations
- [ ] No bare `except:` in `task.py` (use `except Exception:` or more specific)
- [ ] No deprecated typing syntax (`Optional[`, `List[` from `typing`)
- [ ] `uv run python check.py` prints "Mission 02 complete!"
