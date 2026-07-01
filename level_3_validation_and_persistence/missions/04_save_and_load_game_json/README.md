# Mission 04: Save and Load Game JSON

## Goal

Replace the raw-dict save/load with a validated Pydantic model that includes a `schema_version` field, so old save files can be detected and handled cleanly.

## You will learn

- Using Pydantic for data going *out* (saving) as well as coming *in* (loading)
- `model_dump_json()` and `model_validate_json()` for JSON serialisation
- `schema_version` as a forward-compatibility mechanism
- How to raise a meaningful `ValueError` when a save file is outdated

## Game problem

The starter `save_game()` saves a plain dict:

```python
data = {"name": hero.name, "hp": hero.hp, ...}
json.dump(data, f)
```

And `load_game()` reads it back with no validation:

```python
data = json.load(f)
return Hero(name=data["name"], hp=data["hp"], ...)
```

This is fragile in two ways:

1. If the JSON has a wrong type (`"hp": "100"` instead of `"hp": 100`), you get a confusing `TypeError` inside the `Hero` constructor.
2. If you add a new field in a future version of the game, old save files are missing it and the load crashes with a `KeyError`.

Adding `schema_version` to the save model lets you detect the second problem:

```python
if model.schema_version != CURRENT_SCHEMA_VERSION:
    raise ValueError(f"Save version {model.schema_version} is not supported.")
```

## Python concept

Pydantic can also serialise to JSON with `model.model_dump_json()` and parse from JSON with `Model.model_validate_json(text)`. This is more robust than raw `json.dump` / `json.load` because validation runs on both paths.

```python
class SaveGameModel(BaseModel):
    schema_version: int = Field(default=1, ge=1)
    name: str
    hp:   int = Field(ge=0)

# save:
model = SaveGameModel(schema_version=1, name="Ada", hp=100)
path.write_text(model.model_dump_json(indent=2))

# load:
model = SaveGameModel.model_validate_json(path.read_text())
```

## Your task

Open `task.py`.

1. **Complete `SaveGameModel`** — add all Hero fields (`name`, `hero_class`, `hp`, `max_hp`, `atk`, `def_`, `potions`, `gold`, `wins`, `losses`). Store `hero_class` as `str` (use `hero.hero_class.value` when creating the model).

2. **Implement `SaveGameModel.to_hero()`** — convert the model back to a domain `Hero`.

3. **Implement `SaveGameModel.from_hero(hero)`** — create a `SaveGameModel` from a `Hero`.

4. **Implement `save_game(hero, path)`** — call `from_hero()`, then write `model.model_dump_json(indent=2)` to the file.

5. **Implement `load_game(path)`** — return `None` if no file, call `model_validate_json()`, raise `ValueError` if `schema_version` doesn't match, return `model.to_hero()`.

## Run

```bash
uv run python level_3_validation_and_persistence/missions/04_save_and_load_game_json/task.py
```

## Check

```bash
uv run python level_3_validation_and_persistence/missions/04_save_and_load_game_json/check.py
```

## Break it on purpose

Open the generated `saves/save_game.json` and change `"schema_version": 1` to `"schema_version": 2`. Run `load_game()`. You should get a `ValueError` instead of a crash inside the `Hero` constructor.

## Fix it

Bump `CURRENT_SCHEMA_VERSION = 2` in `task.py`. Now the save file matches again — but any file with version 1 would fail. In a real game you would write a migration.

## Side quest

Write a `migrate_save(path: Path) -> None` function that reads version 1 files and upgrades them to version 2 by adding any new default fields.

## Real-world translation

Every database ORM uses migrations for the same reason: schema changes break old data. The `schema_version` field in a JSON save file is a minimal, manual version of the same idea. PostgreSQL uses `pg_dump` format versions; Django uses `python manage.py migrate`.

## Checklist

- [ ] I added all Hero fields to `SaveGameModel`
- [ ] I implemented `to_hero()` and `from_hero()`
- [ ] `save_game()` writes validated JSON with `schema_version`
- [ ] `load_game()` raises `ValueError` when `schema_version` mismatches
- [ ] `load_game()` returns `None` when the file does not exist

---

Next mission: `level_3_validation_and_persistence/missions/05_repository_pattern/README.md`
