# Mission 12: Save Game

## Goal

Save the hero's state to a file and load it back — like a real game save system.

## You will learn

- `import json` — Python's built-in JSON module
- `json.dump(data, file)` — write a dict to a JSON file
- `json.load(file)` — read a JSON file back into a dict
- When to use JSON vs CSV

## Game problem

CSV (Mission 11) works great for flat tabular data like combat logs.
But a hero's save file has nested structure — a dict with multiple fields.
JSON is designed for exactly this: it stores any Python dict faithfully.

```
save_game.json:
{
  "name": "Ada",
  "class": "Warrior",
  "hp": 52,
  "max_hp": 120,
  "level": 1,
  "gold": 75
}
```

## Your task

Open `task.py`. Implement two TODO sections — save and load.

**Saving:**
```python
with open("save_game.json", "w") as f:
    json.dump(hero, f, indent=2)
```

`indent=2` makes the file human-readable (pretty-printed). Without it, everything lands on one line.

**Loading:**
```python
with open("save_game.json", "r") as f:
    loaded_hero = json.load(f)
```

`json.load()` reads the file and returns a Python dict — ready to use.

## Run

```bash
uv run python missions/12_save_game/task.py
```

Then inspect the file:
```bash
cat save_game.json
```

## Check

The check verifies both operations: that the file was saved correctly and that the data was loaded back into `loaded_hero`.

```bash
uv run python missions/12_save_game/check.py
```

## Side quest

JSON supports lists too. Add an inventory to the hero dict:

```python
hero["inventory"] = ["sword", "health potion", "shield"]
```

Save and reload. The list round-trips perfectly through JSON.

---

Next mission: `level_1_python_basics/missions/13_split_the_game/README.md`
