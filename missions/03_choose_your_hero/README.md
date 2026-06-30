# Mission 03: Choose Your Hero

## Goal

Let the player pick a hero class at the start of the game.

## You will learn

- `input()` — reading text from the player
- `if` / `elif` / `else` — branching based on a value
- String comparison and `.strip().lower()` for clean input

## Game problem

Before the battle begins, the player should choose a class.
Each class has different stats — the warrior is tough, the mage hits hard, the rogue is balanced.
The game needs to translate the player's text input into actual numbers.

## Your task

Open `task.py` and complete `choose_hero_class(choice)`.

The function receives a string and should return a dictionary:

| Input        | `"class"` | `"hp"` | `"damage"` | `"bonus"` |
|--------------|-----------|--------|------------|-----------|
| `"warrior"`  | `"Warrior"` | `120` | `15` | `"armor"` |
| `"mage"`     | `"Mage"`    | `80`  | `25` | `"spell"` |
| `"rogue"`    | `"Rogue"`   | `100` | `20` | `"crit"`  |
| anything else | — | — | — | return `None` |

**Reminder — if/elif/else:**

```python
if choice == "warrior":
    return { ... }
elif choice == "mage":
    return { ... }
elif choice == "rogue":
    return { ... }
else:
    return None
```

## Run

```bash
uv run python missions/03_choose_your_hero/task.py
```

Type `warrior`, `mage`, or `rogue` when prompted.

## Check

The check does not use `input()` — it calls your function directly with different values:

```bash
uv run python missions/03_choose_your_hero/check.py
```

## Side quest

What happens if the player types `"Warrior"` with a capital W?

Add `.lower()` to the input line so both `"warrior"` and `"Warrior"` work:

```python
choice = input("> ").strip().lower()
```

The check already passes lowercase — this is about making the game friendlier for real players.

---

Next up: `projects/01_battle_calculator/README.md`
