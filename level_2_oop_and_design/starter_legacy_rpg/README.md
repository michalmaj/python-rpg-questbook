# Starter Legacy RPG

You just joined a team.

Someone before you wrote a working RPG. It runs. Players enjoy it. There are no tests and no documentation, but the combat feels good, the save system works, and customers are happy.

Nobody wants to touch the code.

This isn't literally code you wrote — it's a larger, curated example built entirely from Level 1 constructs (variables, functions, dicts, lists, `random`, CSV, JSON). It represents the kind of program a Level 1 graduate could plausibly produce by extending their game feature by feature, without ever stopping to restructure it. Read it the way you'd read code left behind by someone with exactly your Level 1 skill set — because that's exactly what it is.

---

## How to run it

```bash
uv run python level_2_oop_and_design/starter_legacy_rpg/main.py
```

Play through a fight or two. Save the game. Load it. Make sure you understand what every part does.

---

## One thing Level 1 didn't cover: `global`

Level 1 never used the `global` keyword, but this file leans on it heavily (`choose_hero`, `monster_attacks`, `use_potion`, `run_combat`, `load_game`). Quick primer before you read further:

- Without `global`, assigning to a name inside a function creates a *local* name — it never touches a module-level variable that happens to share the name.
- `global hero_hp` tells Python "this function assigns to the module-level `hero_hp`, not a new local one."
- That's how a line like `hero_hp -= dmg`, buried inside `monster_attacks()`, can change the hero's HP for the whole game.

You don't need to master `global` — you need to recognize it long enough to see the problem it enables: state that any function can reach in and mutate, with no clear owner. That's exactly the kind of shared, mutable global state Level 2 teaches you to replace with objects.

---

## Your job in Level 2

Read `main.py` from top to bottom. As you read, ask yourself:

- What happens if you want to add a second hero (co-op mode)?
- What happens if you want to add a new monster type?
- How would you write a test for `hero_attacks()`?
- Could you use any of this code in a different project?

You probably already see the problems. Level 2 missions will walk you through fixing them, one concept at a time.

---

## What you will refactor

| Problem in the code | Level 2 concept |
|---|---|
| Hero state lives in global variables | Classes and objects |
| Monsters are plain dictionaries | Dataclasses |
| `"warrior"`, `"mage"`, `"rogue"` are magic strings | Enums |
| `hero_attacks()` and `monster_attacks()` share the same formula | Inheritance |
| No type hints anywhere | Type annotations |
| Everything is in one file | Module separation |
| Log is written inside attack functions | Separation of concerns |
| No tests | Pytest with pure functions |

By the end of Level 2, `main.py` will be split into multiple well-named modules, the hero and monsters will be proper classes, and the game logic will be testable in isolation.

The game will work exactly the same. The code will be completely different.

---

**Next:** `level_2_oop_and_design/README.md`
