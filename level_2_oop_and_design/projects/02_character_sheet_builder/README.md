# Project 02: Character Sheet Builder

**Requires:** Level 2, Missions 01–07 (through Dataclasses)

## What you will build

A character sheet system that combines everything from World 2: type hints, enums, dataclasses, and computed properties — all in one clean design.

## What the sheet must have

| Requirement | Concept from |
|---|---|
| `HeroClass` Enum with WARRIOR, MAGE, RANGER | M05 |
| `Weapon` dataclass: `name`, `damage`, `weight` | M07 |
| `Armor` dataclass: `name`, `defense`, `weight` | M07 |
| `CharacterSheet` dataclass with optional `weapon` and `armor` | M07, M04 |
| `total_weight` property — sum of equipped weights, 0.0 if slot empty | M06 |
| `power_score` property — `damage + defense - int(total_weight // 5)`, min 0 | M06 |
| `is_encumbered` property — True when `total_weight > 20.0` | M06 |
| `summary()` method — readable string with name and hero_class | M01 |

## Structure

```
02_character_sheet_builder/
├── README.md    ← this file
├── task.py      ← implement everything here
└── check.py     ← run to verify
```

## How to check

```bash
cd level_2_oop_and_design/projects/02_character_sheet_builder
uv run python check.py
```

## power_score formula

```
power_score = weapon.damage + armor.defense - int(total_weight // 5)
```

- Missing weapon → 0 damage
- Missing armor → 0 defense
- Minimum power_score is 0 (never negative)

## Example

```python
sword = Weapon("Iron Sword", damage=12, weight=3.5)
vest  = Armor("Leather Vest", defense=6, weight=6.0)
ada   = CharacterSheet("Ada", HeroClass.WARRIOR, hp=120, weapon=sword, armor=vest)

ada.total_weight   # 9.5
ada.power_score    # 12 + 6 - int(9.5 // 5) = 17
ada.is_encumbered  # False
ada.summary()      # "Ada [WARRIOR] — HP: 120  Power: 17  Weight: 9.5 kg"
```

---

**Next:** [Project 03 — Refactored RPG (Boss Fight)](../03_refactored_rpg/README.md)
