# Level 2: OOP and Design

**Prerequisite:** Level 1 complete (or equivalent Python fundamentals).

---

## The premise

You finished Level 1. You built a working RPG. It runs, it saves, players enjoy it.

Now open `starter_legacy_rpg/main.py`.

That is the code you wrote. And you already know something is wrong with it.

Level 2 teaches you to name what is wrong — and fix it systematically, using the tools professional Python developers reach for every day: classes, dataclasses, enums, type hints, modules, properties, and tests.

You are not learning abstract object-oriented theory. You are refactoring a real game you already understand.

---

## What you will learn

| Concept | Game meaning |
|---|---|
| Classes and objects | Hero is a first-class object, not scattered globals |
| Dataclasses | Monsters become structured data with defaults |
| Enums | `HeroClass.WARRIOR` replaces `"warrior"` everywhere |
| Inheritance | Hero and Monster share one `Character` base |
| Type hints | Every function says what it expects and returns |
| Properties | `hero.is_alive` instead of `hero.hp > 0` |
| Module separation | `hero.py`, `monster.py`, `combat.py`, `game.py` |
| Pure functions | Combat logic that is testable without a running game |
| Pytest | Tests that catch regressions before players do |

---

## How to start

```bash
# 1. Read the legacy code — understand what it does
uv run python level_2_oop_and_design/starter_legacy_rpg/main.py

# 2. Open the Level 2 course map
#    COURSE_MAP.md → Level 2 section

# 3. Start Mission 01
#    level_2_oop_and_design/missions/01_extract_hero/README.md
```

---

## Worlds

**World 1: Objects** — replace global state with objects (M01–M03)

**World 2: Design** — improve object design (M04–M07)

**World 3: Structure** — split, test, and separate concerns (M08–M10)

**Boss Fight:** Project 01 — assemble everything into a clean, testable, modular RPG
