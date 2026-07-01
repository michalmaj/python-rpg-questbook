# Mission 02: Pydantic Monster Config

## Goal

Replace hand-written validation with Pydantic models — one model definition does the work of dozens of `isinstance` checks.

## You will learn

- Defining a Pydantic `BaseModel`
- `Field(gt=0)`, `Field(ge=0)` for numeric constraints
- `alias` for JSON keys that are Python reserved words (`def`)
- `ValidationError` — what it contains and how to catch it
- Why Pydantic is used at system boundaries, not inside the domain

## Game problem

In Mission 01 you wrote `validate_monster()` by hand. It works, but it is verbose and easy to forget a check. Worse, it returns strings — not structured data you can act on.

Pydantic lets you write the same validation as a type annotation:

```python
from pydantic import BaseModel, Field

class MonsterConfig(BaseModel):
    name: str
    hp:   int = Field(gt=0)   # hp must be greater than 0
    atk:  int = Field(ge=1)   # atk must be >= 1
    def_: int = Field(ge=0, alias="def")
    gold: int = Field(ge=0)
```

Now `MonsterConfig.model_validate(raw_dict)` either returns a valid model or raises `ValidationError` with a precise description of every problem.

## Python concept

Pydantic is a data validation library. A `BaseModel` subclass declares the shape and constraints of data using type annotations. Pydantic enforces them automatically when you construct or parse the model.

```python
from pydantic import BaseModel, Field, ValidationError

class MonsterConfig(BaseModel):
    name: str
    hp:   int = Field(gt=0)

try:
    m = MonsterConfig.model_validate({"name": "Ghost", "hp": -50})
except ValidationError as e:
    print(e)   # shows exactly which field failed and why
```

**`alias`** handles the case where the JSON key is a Python reserved word:

```python
from pydantic import ConfigDict

class MonsterConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    def_: int = Field(ge=0, alias="def")
```

With this, both `{"def": 2}` (JSON) and `def_=2` (Python keyword arg) work.

## Your task

Open `task.py` and define:

1. **`MonsterConfig`** — validates a single monster from `monsters.json`
   - `name: str`
   - `hp: int` — `Field(gt=0)`
   - `atk: int` — `Field(ge=1)`
   - `def_: int` — `Field(ge=0, alias="def")` + `ConfigDict(populate_by_name=True)`
   - `gold: int` — `Field(ge=0)`

2. **`WeaponConfig`** — validates a single weapon from `weapons.json`
   - `name: str`
   - `atk_bonus: int` — `Field(ge=0)`
   - `price: int` — `Field(ge=0)`

Uncomment the lines in `main()` and run the file to see Pydantic in action.

## Run

```bash
uv run python level_3_validation_and_persistence/missions/02_pydantic_monster_config/task.py
```

## Check

```bash
uv run python level_3_validation_and_persistence/missions/02_pydantic_monster_config/check.py
```

## Break it on purpose

Change `Field(gt=0)` to `Field(ge=0)` for `hp`. Now `MonsterConfig.model_validate({"name": "Undead", "hp": 0, ...})` succeeds. A monster with 0 HP enters the game already dead.

## Fix it

Use `gt=0` (strictly greater than) not `ge=0` (greater than or equal). A monster must have at least 1 HP to be alive at spawn.

## Side quest

Add an optional `loot: list[str] | None = None` field to `MonsterConfig`. What does Pydantic do if the JSON contains `"loot": 42` (an int instead of a list)?

## Real-world translation

FastAPI uses Pydantic models as request body schemas — it parses and validates incoming JSON automatically. Django REST Framework uses serializers. Pydantic is now part of the standard Python data-validation stack.

## Checklist

- [ ] I can define a Pydantic `BaseModel` with typed fields
- [ ] I can use `Field(gt=0)` and `Field(ge=0)` for numeric constraints
- [ ] I know how `alias` maps JSON keys to Python field names
- [ ] I can catch `ValidationError` and read its messages
- [ ] I understand that Pydantic is for validation at boundaries, not inside the domain

---

Next mission: `level_3_validation_and_persistence/missions/03_load_game_catalogs/README.md`
