# Mission 01: Extract Hero

## Goal

Replace 10 global hero variables with a single `Hero` class.

## You will learn

- Defining a class with `class`
- Writing `__init__` with parameters
- Storing data as instance attributes (`self.hp`, `self.name`)
- Creating an object from a class

## Game problem

The legacy RPG stores the hero as ten separate global variables:

```python
hero_name = ""
hero_class = ""
hero_hp = 0
hero_max_hp = 0
# ...
```

If you wanted two heroes (co-op mode) you would need twenty variables and double every line of code. Classes solve this.

## Python concept

A **class** is a template. An **object** (or instance) is one thing created from that template.

```python
class Sword:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

# Two swords — same template, different data
iron_sword   = Sword("Iron Sword", 10)
golden_sword = Sword("Golden Sword", 18)

print(iron_sword.damage)   # 10
print(golden_sword.damage) # 18
```

`self` is the object itself. `self.damage = damage` stores the value on this specific object.

## Your task

Open `task.py`. Define a `Hero` class with `__init__` that accepts all hero attributes and stores them as instance attributes. Then create one hero object.

## Run

```bash
uv run python level_2_oop_and_design/missions/01_extract_hero/task.py
```

You should see the hero's stats printed.

## Check

```bash
uv run python level_2_oop_and_design/missions/01_extract_hero/check.py
```

## Break it on purpose

Change `self.hp = hp` to just `hp = hp` (no `self`). Run the check. What error do you get?

## Fix it

Add `self.` back. `self.hp` stores the value on the object. `hp = hp` just reassigns a local variable that disappears immediately.

## Side quest

Add a `__repr__` method to `Hero` that returns a readable string like:
```
Hero(name='Ada', hero_class='warrior', hp=120/120)
```
Hint: `__repr__` is what Python prints when you use `print()` or type the object name in the REPL.

## Real-world translation

Every web framework, database ORM, and game engine uses classes to represent entities. Django's `User`, SQLAlchemy's `Model`, Unity's `MonoBehaviour` — all of these are classes that hold state and behaviour in one place.

## Checklist

- [ ] I can define a class with `class Name:`
- [ ] I can write `__init__` with parameters
- [ ] I understand what `self` refers to
- [ ] I can access attributes with `object.attribute`
- [ ] I can create two different objects from the same class

---

Next mission: `level_2_oop_and_design/missions/02_monster_class/README.md`
