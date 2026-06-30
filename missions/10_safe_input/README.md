# Mission 10: Safe Input

## Goal

Keep the game alive when a player types something unexpected.

## You will learn

- `try` / `except` — catch an error before it crashes the program
- `ValueError` — the error Python raises when a conversion fails
- Why real programs never trust raw input

## Game problem

`int(input())` crashes if the player types `"banana"` instead of a number.
A game that crashes on bad input is broken.
`try/except` lets you handle the error and continue:

```python
raw = input("> ")

try:
    monster_hp = int(raw)     # might raise ValueError
except ValueError:
    monster_hp = 100          # fallback if conversion fails
```

## Your task

Open `task.py`. Implement the `try/except` block so that:
- A valid number (e.g. `"75"`) → `monster_hp = 75`
- Any non-number (e.g. `"banana"`) → `monster_hp = 100`

**How try/except works:**

```
try:
    <code that might fail>
except <ErrorType>:
    <code that runs only if the error occurred>
```

Python tries the `try` block first.
If a `ValueError` is raised, it jumps to `except` and runs that block instead.
If no error occurs, the `except` block is skipped entirely.

## Run

```bash
uv run python missions/10_safe_input/task.py
```

Try it twice — once with a number, once with a word.

## Check

The check runs your script with different inputs and reads the output:

```bash
uv run python missions/10_safe_input/check.py
```

## Side quest

Add a message inside the `except` block so the player knows what happened:

```python
except ValueError:
    print(f"'{raw}' is not a number — using default HP of 100.")
    monster_hp = 100
```

Then try a third input type: what happens with `"3.5"` (a float as a string)?
`int()` cannot convert `"3.5"` directly — it raises `ValueError` too.

---

Next up: `projects/03_terminal_rpg/README.md`
