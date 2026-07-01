# Mission 04: Type Hints

## Goal

Add type annotations to every function and method in the refactored code.

## You will learn

- Parameter type hints: `def attack(target: Character) -> int:`
- Return type hints: `-> bool`, `-> None`, `-> int`
- Annotating attributes in `__init__`
- How mypy (and editors) use hints to catch bugs before you run the code

## Game problem

The legacy RPG has no type hints:

```python
def hero_attacks(monster):
    ...
```

Is `monster` a dict? A Monster object? What does the function return? You have to read the whole body to find out.

Type hints make the contract explicit:

```python
def compute_damage(attacker: Character, target: Character) -> int:
    ...
```

Now any editor, type checker, or team member knows immediately.

## Python concept

Type hints are optional annotations after `:` for parameters and after `->` for return types. Python does not enforce them at runtime — they are for humans and tools.

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def level_up(hero: Hero, amount: int) -> None:
    hero.atk += amount
```

For attributes in `__init__`:

```python
class Hero:
    def __init__(self, name: str, hp: int, atk: int) -> None:
        self.name: str = name
        self.hp:   int = hp
        self.atk:  int = atk
```

The `: int` after `self.hp` annotates the attribute type. It is optional but helpful.

## Your task

Open `task.py`. The `Character`, `Hero`, and `Monster` classes from Mission 03 are provided without type hints. Add hints to every parameter, return type, and attribute.

> **Heads-up — there is an intentional logic bug in `use_potion`:**
> ```python
> self.hp = min(self.hp + heal_amount, self.hp)   # always evaluates to self.hp
> ```
> Type hints will not catch this — the types are all correct (`int + int`, `min(int, int)`).
> This is deliberate: it shows that type hints verify *types*, not *logic*.
> You will write a test that catches this kind of bug in Mission 10.
> Leave the bug in place for now — your task is type annotations only.

## Run

```bash
uv run python level_2_oop_and_design/missions/04_type_hints/task.py
```

(If installed) check with mypy:

```bash
uv run mypy level_2_oop_and_design/missions/04_type_hints/task.py --ignore-missing-imports
```

## Check

```bash
uv run python level_2_oop_and_design/missions/04_type_hints/check.py
```

## Break it on purpose

Call `hero.take_damage("lots")` — a string instead of an int. Python will not complain at runtime until the subtraction fails. Type hints would have caught this in an editor before you even ran the code.

## Fix it

Always pass `int` to `take_damage`. Type hints document the rule; a type checker enforces it.

## Side quest

Install mypy and run it on `task.py`. Fix any errors it finds. Note that mypy is stricter than Python itself — it is like a spell-checker for types.

## Real-world translation

FastAPI uses type hints to automatically validate request bodies, generate API documentation, and provide editor autocomplete. Django REST Framework uses them for serializer fields. Type hints went from optional nicety to professional necessity.

## Checklist

- [ ] I can annotate function parameters with types
- [ ] I can annotate return types with `->`
- [ ] I know that `-> None` means the function returns nothing
- [ ] I can annotate attributes inside `__init__`
- [ ] I understand that hints are checked by tools, not Python itself

---

Next mission: `level_2_oop_and_design/missions/05_enums/README.md`
