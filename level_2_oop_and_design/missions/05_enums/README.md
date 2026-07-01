# Mission 05: Enums

## Goal

Replace magic strings `"warrior"`, `"mage"`, `"rogue"` with a `HeroClass` enum.

## You will learn

- Defining an `Enum` class
- Using enum values instead of string literals
- Why enums prevent typos and make invalid states unrepresentable

## Game problem

The legacy RPG uses strings to represent hero classes:

```python
if hero_class == "warrior":
    bonus = 2
elif hero_class == "mage":
    bonus = 0
elif hero_class == "rogue":
    bonus = roll(4)
```

Nothing stops you from writing `"Warrior"` (capital W) or `"warior"` (typo) — Python will silently fall through all branches. Enums make invalid values impossible.

## Python concept

An **enum** (enumeration) is a fixed set of named values.

```python
from enum import Enum

class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST  = "east"
    WEST  = "west"

player_direction = Direction.NORTH

if player_direction == Direction.NORTH:
    print("Moving north")
```

You cannot write `Direction.NROTH` by accident — Python raises `AttributeError` immediately.

```python
Direction("northeast")   # ValueError — not a valid value
Direction.NORTHEAST      # AttributeError — not a valid member
```

## Your task

Open `task.py`. Define a `HeroClass` enum with members `WARRIOR`, `MAGE`, and `ROGUE`. Then update `Hero.__init__` to accept `hero_class: HeroClass` instead of a plain string. Update the `class_bonus()` method to use enum comparison.

## Run

```bash
uv run python level_2_oop_and_design/missions/05_enums/task.py
```

## Check

```bash
uv run python level_2_oop_and_design/missions/05_enums/check.py
```

## Break it on purpose

Try `Hero("Ada", hp=120, atk=15, def_=8, potions=2, gold=20, hero_class="warrior")`.
Notice that nothing prevents passing a raw string. Now try accessing `HeroClass("warior")`.
What error do you get?

## Fix it

Always use `HeroClass.WARRIOR` — never the raw string `"warrior"`. The enum is the only valid way to specify a class.

## Side quest

Add a `MonsterTier` enum with values `WEAK`, `NORMAL`, `ELITE`, `BOSS`. Assign a tier to each monster in the MONSTERS table. Then add a `damage_multiplier` property that returns `1.0`, `1.2`, `1.5`, or `2.0` based on tier.

## Real-world translation

Django's model field choices, SQLAlchemy column enums, HTTP status codes — all of these use enums or enum-like patterns. `http.HTTPStatus.OK` is clearer than the magic number `200` everywhere.

## Checklist

- [ ] I can import and define an `Enum` subclass
- [ ] I can use enum members in comparisons (`hero_class == HeroClass.WARRIOR`)
- [ ] I understand that typos cause `AttributeError`, not silent bugs
- [ ] I can use an enum value as a type hint
- [ ] I know that `SomeEnum("value")` converts a string to an enum member

---

Next mission: `level_2_oop_and_design/missions/06_properties/README.md`
