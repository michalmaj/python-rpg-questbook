# Mission 03: Character Base

## Goal

Identify duplicated logic in `hero_attacks()` and `monster_attacks()`, then extract it into a shared `Character` base class.

## You will learn

- Inheritance: one class extending another
- The `super().__init__()` call
- Overriding methods in a subclass
- Sharing logic between classes without copy-pasting

## Game problem

Hero and Monster share the same fundamental state: a name, HP, attack power, and defence. They also share the same behaviour: they can take damage, and they can be alive or dead.

Right now both classes store this separately, with no connection between them. Add a third class `Character` as the base, and both `Hero` and `Monster` get those shared attributes and methods for free.

> **Note on the damage formula:** `hero_attacks()` and `monster_attacks()` also look similar, but the right tool there is a **pure function** (`compute_damage`), not inheritance. Inheritance is for shared *identity* — things that are genuinely the same kind of thing. A formula is a rule, not an identity. You will extract `compute_damage` in Mission 09.
>
> Rule of thumb: if two classes *are* the same kind of thing (both are characters), use inheritance. If two functions *do* the same calculation, extract a function.

## Python concept

**Inheritance** lets one class reuse code from another.

```python
class Character:
    def __init__(self, name, hp, atk, def_):
        self.name = name
        self.hp   = hp
        self.atk  = atk
        self.def_ = def_

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)


class Hero(Character):
    def __init__(self, name, hp, atk, def_, potions):
        super().__init__(name, hp, atk, def_)   # call parent __init__
        self.potions = potions                   # Hero-specific attribute


class Monster(Character):
    def __init__(self, name, hp, atk, def_, gold):
        super().__init__(name, hp, atk, def_)
        self.gold = gold
```

Now `is_alive()` and `take_damage()` are written once, in `Character`, and available to both `Hero` and `Monster` automatically.

## Your task

Open `task.py`. Define three classes:

1. `Character` — base class with `name`, `hp`, `atk`, `def_`; methods `is_alive()` and `take_damage(amount)`
2. `Hero(Character)` — adds `potions` and `gold`
3. `Monster(Character)` — adds `gold`

## Run

```bash
uv run python level_2_oop_and_design/missions/03_character_base/task.py
```

## Check

```bash
uv run python level_2_oop_and_design/missions/03_character_base/check.py
```

## Break it on purpose

Remove `super().__init__(name, hp, atk, def_)` from `Hero.__init__`. Then create a hero and call `hero.is_alive()`. What error do you get?

## Fix it

Without `super().__init__()`, the parent's `__init__` never runs, so `self.hp` is never set. `is_alive()` fails because it tries to read `self.hp` which does not exist.

## Side quest

Add a `roll_damage(target)` method to `Character` that returns:
```python
max(1, self.atk + random.randint(1, 6) - target.def_)
```
Both `Hero` and `Monster` inherit it automatically. Try calling `hero.roll_damage(monster)` and `monster.roll_damage(hero)` — they both work.

## Real-world translation

Django's `Model` base class gives every model `save()`, `delete()`, and `objects.filter()`. You never write those methods yourself. You inherit them. That is inheritance at scale.

## Checklist

- [ ] I can define a base class with shared attributes and methods
- [ ] I can write a subclass using `class Child(Parent):`
- [ ] I understand why `super().__init__()` is needed
- [ ] I know that subclasses inherit parent methods automatically
- [ ] I can add subclass-specific attributes in `__init__`

---

Next mission: `level_2_oop_and_design/missions/04_type_hints/README.md`
