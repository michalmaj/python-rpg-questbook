# Mission 03: Load Game Catalogs

## Goal

Complete the full pipeline from external JSON to a domain object:

```
monsters.json  →  MonsterConfig (Pydantic)  →  Monster (dataclass)
weapons.json   →  WeaponConfig  (Pydantic)  →  Weapon  (dataclass)
```

## You will learn

- The boundary pattern: Pydantic at the edge, dataclass inside the domain
- `to_domain()` as a conversion method on a Pydantic model
- How to load a whole catalog and skip invalid entries gracefully
- Why the game domain should never import Pydantic

## Game problem

After Mission 02 you can validate a single monster dict. Now the game needs to load all monsters and all weapons at startup, convert them to usable domain objects, and handle any bad entries without crashing.

The clean way to do this separates two concerns:

- **Pydantic model** — knows the JSON format, validates constraints, raises `ValidationError`
- **domain dataclass** — knows the game logic, works inside combat, is passed to functions

The Pydantic model converts *itself* into a domain object:

```python
class MonsterConfig(BaseModel):
    ...
    def to_domain(self) -> Monster:
        return Monster(name=self.name, hp=self.hp, atk=self.atk,
                       def_=self.def_, gold=self.gold)
```

Game code calls `load_monsters()` and gets back `list[Monster]` — it never sees Pydantic.

## Python concept

**`to_domain()`** is a factory method on a Pydantic model. It converts validated, external data into a clean domain object. This is the boundary: Pydantic stays on the outside, dataclasses stay inside.

```python
from pydantic import BaseModel

class MonsterConfig(BaseModel):
    name: str
    hp: int

    def to_domain(self) -> Monster:
        return Monster(name=self.name, hp=self.hp, ...)
```

**Graceful skip pattern** for loading catalogs:

```python
from pydantic import ValidationError

results = []
for entry in raw["monsters"]:
    try:
        config = MonsterConfig.model_validate(entry)
        results.append(config.to_domain())
    except ValidationError as e:
        print(f"  ⚠ Skipped {entry.get('name', '?')}: {e}")
```

A bad entry does not crash the whole load — it prints a warning and continues.

## Your task

Open `task.py`. `MonsterConfig` and `WeaponConfig` are already defined (from Mission 02).

Implement:

1. **`MonsterConfig.to_domain()`** — return a `Monster` using `self.name`, `self.hp`, etc.
2. **`WeaponConfig.to_domain()`** — return a `Weapon`
3. **`load_monsters(path)`** — read `monsters.json`, validate each entry, return `list[Monster]`; skip invalid entries with a warning
4. **`load_weapons(path)`** — same pattern for `weapons.json`

## Run

```bash
uv run python level_3_validation_and_persistence/missions/03_load_game_catalogs/task.py
```

## Check

```bash
uv run python level_3_validation_and_persistence/missions/03_load_game_catalogs/check.py
```

## Break it on purpose

Add a bad entry to `monsters.json`:

```json
{"name": "Broken", "hp": -1, "atk": 5, "def": 2, "gold": 0}
```

Run `load_monsters()`. The broken monster should be skipped with a warning. The rest of the list should still load.

## Fix it

Remove the bad entry. Your `load_monsters()` already handles this because of the `try/except ValidationError` pattern.

## Side quest

Add a `HeroClassConfig` Pydantic model for `hero_classes.json`, and a `load_hero_classes()` function that returns a `dict[str, HeroClassStats]` (where `HeroClassStats` is a domain dataclass with `hp`, `atk`, `def_`).

## Real-world translation

This `to_domain()` pattern maps directly to the **Anti-Corruption Layer** in Domain-Driven Design. The idea: external data formats (JSON, XML, database rows) are "corrupt" from the domain's perspective. You translate them at the boundary and keep the domain clean.

## Checklist

- [ ] I implemented `to_domain()` on both Pydantic models
- [ ] I understand that `to_domain()` converts external format → domain object
- [ ] I implemented `load_monsters()` that skips invalid entries gracefully
- [ ] I understand why game logic should never import from Pydantic
- [ ] I can explain: what is the "boundary" between Pydantic and the domain?

---

Next mission: `level_3_validation_and_persistence/missions/04_save_and_load_game_json/README.md`
