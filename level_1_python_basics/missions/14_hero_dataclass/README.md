# Mission 14: Hero Dataclass

## Goal

Upgrade the hero from a plain dict to a structured dataclass — typed fields, dot-access, and auto-generated printing.

## You will learn

- `from dataclasses import dataclass` — Python's built-in dataclass tool
- `@dataclass` — a decorator that turns a class definition into a ready-to-use data structure
- Type annotations (`name: str`, `hp: int`) — how Python knows what type each field should hold
- Dot access (`hero.hp`) vs dict access (`hero["hp"]`)

## Game problem

The hero dict from Mission 12 works, but it has problems:

```python
hero = {"name": "Ada", "hp": 100}
hero["hP"] += 10   # typo — no error, just a mystery new key
```

Python has no way to tell you that `"hP"` is wrong. A dataclass catches this:

```python
hero.hP += 10   # AttributeError: 'Hero' object has no attribute 'hP'
```

Structured data → fewer bugs.

## Python concept

A **dataclass** is a class where Python auto-generates `__init__` and `__repr__` for you based on the fields you declare:

```python
from dataclasses import dataclass

@dataclass
class Hero:
    name: str
    hp: int
    max_hp: int

hero = Hero(name="Ada", hp=100, max_hp=100)
print(hero)        # Hero(name='Ada', hp=100, max_hp=100)
print(hero.hp)     # 100
hero.hp -= 30
print(hero.hp)     # 70
```

You define the fields with a **type annotation** (`name: str`). The annotation tells Python — and you — what kind of data belongs in each field. Python does not enforce the types at runtime, but your editor and check tools will warn you if you put the wrong type in.

## Your task

Open `task.py`. Three TODOs:

1. Create a `Hero` with `name="Ada"`, `hero_class="Warrior"`, `hp=100`, `max_hp=100`, `level=1`, `gold=50`
2. Subtract 30 from `hero.hp`
3. Add 25 to `hero.gold`

Expected output:
```
Name:  Ada
Class: Warrior
HP:    70/100
Gold:  75
```

## Run

```bash
uv run python missions/14_hero_dataclass/task.py
```

## Check

```bash
uv run python missions/14_hero_dataclass/check.py
```

## Side quest

Dataclasses print themselves for free:

```python
print(hero)
# Hero(name='Ada', hero_class='Warrior', hp=70, max_hp=100, level=1, gold=75)
```

Try adding `print(hero)` to the bottom of `task.py` before running it. Then try the same thing with the dict from Mission 12 — you get `{'name': 'Ada', ...}`, which works but is harder to read.

## Break it

Try accessing a field that doesn't exist:

```python
print(hero.mana)
```

You get `AttributeError: 'Hero' object has no attribute 'mana'`. This is Python telling you the field doesn't exist — much clearer than a dict silently returning `None` (or crashing with `KeyError`).

## Fix it

Remove the bad access. The Hero has exactly the fields you declared.

## Real-world translation

Dataclasses are used everywhere Python needs structured data: API responses, database rows, config objects. Libraries like Pydantic and attrs are built on the same idea — declare your fields, get safety and structure for free.

---

Next mission: `level_1_python_basics/missions/15_test_the_damage/README.md`
