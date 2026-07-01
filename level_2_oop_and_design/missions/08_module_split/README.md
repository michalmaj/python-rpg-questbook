# Mission 08: Module Split

## Goal

Split the legacy `main.py` into four focused modules: `hero.py`, `monster.py`, `combat.py`, and `game.py`.

## You will learn

- How to split a large file into multiple modules
- How to import from a module in the same package
- What a package is (`__init__.py`)
- The principle of single responsibility

## Game problem

The legacy `main.py` has 200 lines and does everything:
defines monsters, manages hero state, handles combat, saves files, and runs the main loop.

When you want to change the damage formula, you have to search through combat menus and save logic to find it. When a new teammate joins, they have to read the whole file to understand any one part.

**Single responsibility principle:** each module should do one thing.

## Python concept

Python files are modules. When files live in the same folder, you import between them:

```
rpg/
├── __init__.py     # makes rpg/ a package (can be empty)
├── hero.py         # Hero class
├── monster.py      # Monster class and templates
├── combat.py       # damage calculation, combat loop
└── game.py         # main menu, game loop
```

```python
# combat.py
from rpg.hero import Hero
from rpg.monster import Monster

def compute_damage(attacker: Hero, target: Monster) -> int:
    ...
```

An empty `__init__.py` tells Python "this directory is a package". Then you can import across files with `from package.module import SomeClass`.

## Your task

Open `task.py`. You will find four partially filled module stubs. Connect them:

1. `hero.py` — `Hero` class (from Mission 03 + type hints + properties)
2. `monster.py` — `Monster` class and `MONSTER_TEMPLATES` list
3. `combat.py` — `compute_damage(attacker, target)` pure function
4. `game.py` — imports from the other three; contains `main()`

Your task is to fill in the `compute_damage` function in `combat.py` and make the imports work.

## Run

```bash
uv run python level_2_oop_and_design/missions/08_module_split/task.py
```

## Check

```bash
uv run python level_2_oop_and_design/missions/08_module_split/check.py
```

## Break it on purpose

Remove `__init__.py` from the `rpg/` folder and try the import again. What error do you get?

## Fix it

Add an empty `__init__.py` back. Python needs it to treat the directory as a package.

## Side quest

Add a `config.py` module to `rpg/` that defines constants:
```python
CRIT_ROLL = 20
DICE_SIDES = 6
POTION_HEAL = 30
```
Import these constants in `combat.py` instead of magic numbers.

## Real-world translation

Every Python package you install (`requests`, `numpy`, `django`) is a directory with an `__init__.py` and many sub-modules. Your game is becoming a package.

## Checklist

- [ ] I know that a Python file is a module
- [ ] I can create a package with `__init__.py`
- [ ] I can import a class from another module in the same package
- [ ] I understand the single responsibility principle
- [ ] I can split a large file without breaking the program

---

Next mission: `level_2_oop_and_design/missions/09_pure_functions/README.md`
