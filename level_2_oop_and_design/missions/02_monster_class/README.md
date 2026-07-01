# Mission 02: Monster Class

## Goal

Replace monster dictionaries with a `Monster` class. Add a method to the class.

## You will learn

- Defining methods (functions inside a class)
- The difference between attributes (data) and methods (behaviour)
- What `self` means inside a method
- How objects encapsulate state and behaviour together

## Game problem

The legacy RPG stores monsters like this:

```python
{"name": "Goblin", "hp": 30, "atk": 8, "def": 2, "gold": 10}
```

A dictionary can hold data but it cannot have behaviour. You cannot write `monster.attack()` on a dict. To add methods — like `is_alive()` or `take_damage()` — you need a class.

## Python concept

A **method** is a function defined inside a class. It always receives `self` as its first argument.

```python
class Goblin:
    def __init__(self, hp):
        self.hp = hp

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp -= amount

g = Goblin(hp=30)
g.take_damage(10)
print(g.is_alive())  # True  (hp is now 20)
```

The method lives on the class. `self` gives it access to the object's data.

## Your task

Open `task.py`. Define a `Monster` class with:

- `__init__` accepting `name`, `hp`, `atk`, `def_`, `gold`
- An `is_alive()` method returning `True` if `hp > 0`
- A `take_damage(amount)` method that reduces `hp` by `amount` (minimum 0)

Then create three monster objects from the table in the legacy code.

## Run

```bash
uv run python level_2_oop_and_design/missions/02_monster_class/task.py
```

## Check

```bash
uv run python level_2_oop_and_design/missions/02_monster_class/check.py
```

## Break it on purpose

In `take_damage`, write `hp -= amount` instead of `self.hp -= amount`. Run the check. What happens?

## Fix it

Without `self.hp`, Python looks for a local variable called `hp` (which does not exist) or creates one that disappears immediately. `self.hp` refers to the attribute on the object.

## Side quest

Add a `__repr__` method that returns:
```
Monster(name='Goblin', hp=30, atk=8, def_=2)
```

Then add a `description()` method that prints a battle-ready summary:
```
Goblin — HP: 25/30 | ATK: 8 | DEF: 2
```
Note: for `description()` you will need to store `max_hp` as well.

## Real-world translation

Django models use methods like `is_active()`, `get_full_name()`, and `save()`. SQLAlchemy ORM objects have `query()`, `filter()`, `all()`. In all cases, data and behaviour live together.

## Checklist

- [ ] I can define a method inside a class
- [ ] I understand why `self` is the first parameter of every method
- [ ] I can call `object.method()` from outside the class
- [ ] I can write a method that modifies an attribute
- [ ] I can write a method that returns a computed value

---

Next mission: `level_2_oop_and_design/missions/03_character_base/README.md`
