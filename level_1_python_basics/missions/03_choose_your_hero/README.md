# Mission 03: Choose Your Hero

## Goal

Let the player pick a hero class at the start of the game.

## You will learn

- `input()` — reading text from the player
- `if` / `elif` / `else` — branching based on a value
- String comparison and `.strip().lower()` for clean input

## Game problem

Before the battle begins, the player should choose a class.
Each class has different stats — the warrior is tough, the mage hits hard, the rogue is fast.
The game needs to translate the player's text input into actual numbers.

## Your task

Open `task.py`. After the `input()` line you will see four variables set to `None`.
Use `if` / `elif` / `elif` / `else` to set them based on `hero_class`:

| Input       | `hero_name`  | `hero_hp` | `hero_damage` | `hero_bonus` |
|-------------|--------------|-----------|---------------|--------------|
| `"warrior"` | `"Warrior"`  | `120`     | `15`          | `"armor"`    |
| `"mage"`    | `"Mage"`     | `80`      | `25`          | `"spell"`    |
| `"rogue"`   | `"Rogue"`    | `100`     | `20`          | `"crit"`     |

**Reminder — if/elif/else:**

```python
if hero_class == "warrior":
    hero_name = "Warrior"
    hero_hp = 120
    hero_damage = 15
    hero_bonus = "armor"
elif hero_class == "mage":
    # ...
elif hero_class == "rogue":
    # ...
else:
    pass  # hero_name stays None → the error message below will print
```

## Run

```bash
uv run python missions/03_choose_your_hero/task.py
```

Type `warrior`, `mage`, or `rogue` when prompted.

## Check

The check runs your script three times with different inputs and reads the output:

```bash
uv run python missions/03_choose_your_hero/check.py
```

## Side quest

The input line already has `.strip().lower()` — so `"Warrior"` and `"WARRIOR"` both become `"warrior"` before the `if` check. Try it: run the script and type `Warrior` with a capital W. It should work!

---

Next up: `level_1_python_basics/projects/01_battle_calculator/README.md`
