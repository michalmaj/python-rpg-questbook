# Mission 07: Monster Dictionary

## Goal

Group a monster's stats into one dictionary instead of separate variables.

## You will learn

- Dictionaries — key-value pairs that keep related data together
- Creating a dict with `{}`
- Reading a value: `monster["hp"]`
- Updating a value: `monster["hp"] = new_value`

## Game problem

In Mission 01 the hero had four separate variables: `hero_name`, `hero_hp`, `hero_damage`, `hero_gold`.
That works for one hero — but imagine tracking ten different monsters with separate variables each.
A dictionary groups everything under one name:

```python
# Old way — separate variables
monster_name = "Dragon"
monster_hp = 150
monster_damage = 25

# New way — one dictionary
monster = {
    "name": "Dragon",
    "hp": 150,
    "damage": 25,
}
```

## Your task

Open `task.py`. Fill in the four `None` values, then update `monster["hp"]` after a hit.

**Reading and updating a dict:**

```python
print(monster["name"])          # read a value
monster["hp"] = monster["hp"] - 30   # update a value
```

| Key        | Value      | Type  |
|------------|------------|-------|
| `"name"`   | `"Dragon"` | `str` |
| `"hp"`     | `150`      | `int` |
| `"damage"` | `25`       | `int` |
| `"reward"` | `100`      | `int` |

After filling in the dict: update `monster["hp"]` so it reflects 30 damage taken.
HP cannot go below 0.

## Run

```bash
uv run python missions/07_monster_dictionary/task.py
```

Expected output:
```
A wild Dragon appears!
HP:     150
Damage: 25
Reward: 100 gold

After the hero strikes: Dragon has 120 HP remaining.
```

## Check

```bash
uv run python missions/07_monster_dictionary/check.py
```

## Side quest

Add a new key to the monster dictionary:

```python
monster["is_alive"] = monster["hp"] > 0
print(monster["is_alive"])   # True or False
```

You can store any type as a value — including booleans.

---

Next mission: `level_1_python_basics/missions/08_attack_function/README.md`
