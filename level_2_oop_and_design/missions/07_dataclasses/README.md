# Mission 07: Dataclasses

## Goal

Replace a hand-written `Monster.__init__` with `@dataclass`. Understand what the decorator generates automatically.

## You will learn

- The `@dataclass` decorator from the standard library
- What `__init__`, `__repr__`, and `__eq__` mean and when you get them for free
- Default field values with `field(default=...)`
- When to use a dataclass vs a plain class

## Game problem

Every monster in the legacy RPG is a plain dictionary:

```python
{"name": "Goblin", "hp": 30, "atk": 8, "def": 2, "gold": 10}
```

You already replaced this with a class in Mission 02. But writing `__init__` for every data-heavy class is tedious. Dataclasses generate it for you.

## Python concept

`@dataclass` reads the class-level type annotations and generates `__init__`, `__repr__`, and `__eq__` automatically.

```python
from dataclasses import dataclass

@dataclass
class Weapon:
    name:   str
    damage: int
    weight: float = 1.0   # default value

sword = Weapon("Iron Sword", damage=10)
print(sword)              # Weapon(name='Iron Sword', damage=10, weight=1.0)
print(sword.damage)       # 10

axe = Weapon("Axe", 14, 2.5)
sword2 = Weapon("Iron Sword", 10)
print(sword == sword2)    # True — __eq__ compares all fields
```

Without `@dataclass` you would write all three methods by hand. With it, you declare the fields and get everything else for free.

## Your task

Open `task.py`. Convert `MonsterTemplate` (a class representing a monster type, with fixed stats) into a dataclass. Then create four monster templates from the legacy MONSTERS table.

## Run

```bash
uv run python level_2_oop_and_design/missions/07_dataclasses/task.py
```

## Check

```bash
uv run python level_2_oop_and_design/missions/07_dataclasses/check.py
```

## Break it on purpose

Remove the type annotations from the dataclass fields (leave just the names). What happens?

## Fix it

`@dataclass` reads type annotations to discover fields. Without annotations, it cannot generate anything. All fields must be annotated: `name: str`, `hp: int`, etc.

## Side quest

Make `MonsterTemplate` frozen (add `@dataclass(frozen=True)`). Now try `goblin_template.hp = 99`. What error do you get? Frozen dataclasses are immutable — useful for templates that should never change after creation.

## Real-world translation

Python's standard library uses dataclasses for `ast.AST` nodes. FastAPI uses them (via Pydantic, which extends the idea) for request/response models. `@dataclass` is the go-to for simple data containers.

## Checklist

- [ ] I can apply `@dataclass` to a class
- [ ] I understand that `@dataclass` requires type annotations on every field
- [ ] I know that `@dataclass` generates `__init__`, `__repr__`, and `__eq__`
- [ ] I can add a default value to a field
- [ ] I know when to use a dataclass vs a regular class

---

Next mission: `level_2_oop_and_design/missions/08_module_split/README.md`
