# Mission 01: External Data Is Untrusted

## Goal

Discover what happens when game data comes from a JSON file that nobody validated, then write a manual validator to detect the problems.

## You will learn

- Why raw `json.load()` is dangerous at system boundaries
- What kinds of errors can hide in "valid" JSON
- How to write a defensive validation function
- Why this problem motivates Pydantic (Mission 02)

## Game problem

The starter RPG loads monster data like this:

```python
with open("monsters.json") as f:
    raw = json.load(f)

for entry in raw["monsters"]:
    monster = Monster(name=entry["name"], hp=entry["hp"], ...)
```

This works fine when the file is correct. But what if someone (or a bug, or a future collaborator) edits the file and introduces a mistake?

Open `broken_monsters.json`. It contains five monsters:

| Monster | Problem |
|---------|---------|
| Goblin  | valid |
| Ghost   | `hp` is `-50` — a monster that starts dead |
| Slime   | `hp` is `"lots"` — a string, not an int |
| Bandit  | `hp` field is missing entirely |
| Ogre    | has an unknown extra field `secret_power` |

The naive loader in `task.py` (`naive_load()`) will either crash, produce wrong results, or silently accept the bad data. Run it and see.

## Python concept

JSON is just text. `json.load()` gives you Python dicts and lists with no type guarantees. The values can be anything: strings where you expected ints, `None` where you expected a value, missing keys, extra keys.

Validation means checking that the data matches the shape and constraints you expect **before** you use it.

```python
def validate_monster(raw: dict) -> list[str]:
    errors = []
    if "hp" not in raw:
        errors.append("hp: missing")
    elif not isinstance(raw["hp"], int):
        errors.append(f"hp: must be int, got {type(raw['hp']).__name__}")
    elif raw["hp"] <= 0:
        errors.append(f"hp: must be > 0, got {raw['hp']}")
    return errors
```

## Your task

Open `task.py`. `naive_load()` is already written — run it first and read the error or output.

Then implement `validate_monster(raw: dict) -> list[str]`:

- Returns a list of error strings, one per problem
- Returns `[]` if the monster is valid
- Must check: `name` (str), `hp` (int, > 0), `atk` (int, ≥ 1), `def` (int, ≥ 0), `gold` (int, ≥ 0)
- An unknown extra field is **not** an error — extra fields are harmless here

## Run

```bash
uv run python level_3_validation_and_persistence/missions/01_external_data_is_untrusted/task.py
```

## Check

```bash
uv run python level_3_validation_and_persistence/missions/01_external_data_is_untrusted/check.py
```

## Break it on purpose

Edit `broken_monsters.json` and change the Goblin's `hp` to `null`. Run your validator. Does it catch it?

## Fix it

Add a check: `elif raw["hp"] is None:` — or simply rely on `isinstance(raw["hp"], int)` since `None` is not an int.

## Side quest

Extend your validator to check that `name` is a non-empty string (not `""` or `"   "`).

## Real-world translation

Every API endpoint, config file, user upload, and database record that arrives from outside your system is untrusted. Professional backends always validate input at the boundary before touching the domain. In Python, the modern tool for this is Pydantic — which you will meet in Mission 02.

## Checklist

- [ ] I ran `naive_load()` and saw what crashes or goes wrong
- [ ] I understand why raw JSON cannot be trusted
- [ ] I implemented `validate_monster()` that checks types and constraints
- [ ] I know that returning a list of strings is one clean pattern for collecting multiple errors

---

Next mission: `level_3_validation_and_persistence/missions/02_pydantic_monster_config/README.md`
