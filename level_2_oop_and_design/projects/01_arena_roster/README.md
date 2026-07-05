# Project 01: Arena Roster

**Requires:** Level 2, Missions 01–03 (Extract Hero, Monster Class, Character Base)

## What you will build

A small roster of arena combatants. This is your first time designing several classes that work together from scratch — no starter code to copy, just the spec below.

## What the roster must have

| Requirement | Concept from |
|---|---|
| `Character` base class with `name`, `hp`, `max_hp`, `atk`, `def_` | M01, M03 |
| `take_damage(amount)` — reduces HP, never below 0 | M01 |
| `is_alive` property — True if HP > 0 | M01, M06 concept preview |
| `Hero(Character)` with `hero_class` and `potions` | M01, M03 |
| `Monster(Character)` with `reward_gold` | M02, M03 |
| `build_roster()` — returns ≥3 characters (mix of Hero and Monster) | M03 |
| `print_roster(roster)` — prints each character's name, type, and HP | M01 |

## Structure

```
01_arena_roster/
├── README.md    ← this file
├── task.py      ← implement everything here
└── check.py     ← run to verify
```

## How to check

```bash
cd level_2_oop_and_design/projects/01_arena_roster
uv run python check.py
```

## Where to start

1. Implement `Character.__init__` — store `name`, `hp`, `max_hp`, `atk`, `def_`
2. Implement `take_damage` — subtract from `hp`, clamp to 0
3. Implement `is_alive` — return `self.hp > 0`
4. Implement `Hero.__init__` — call `super().__init__`, store extra fields
5. Implement `Monster.__init__` — same pattern
6. Implement `build_roster` — return a list with at least 1 Hero and 1 Monster
7. Implement `print_roster` — loop and print each character

## Example output

```
[Hero]    Ada      HP: 120/120
[Hero]    Zara     HP: 80/80
[Monster] Goblin   HP: 30/30
[Monster] Dragon   HP: 200/200
```

---

**Next:** [Project 02 — Character Sheet Builder](../02_character_sheet_builder/README.md)
