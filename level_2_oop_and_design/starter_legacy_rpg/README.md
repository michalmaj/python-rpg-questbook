# Starter Legacy RPG

You just joined a team.

Someone before you wrote a working RPG. It runs. Players enjoy it. There are no tests and no documentation, but the combat feels good, the save system works, and customers are happy.

Nobody wants to touch the code.

That someone is you — six months ago, right after finishing Level 1.

---

## How to run it

```bash
uv run python level_2_oop_and_design/starter_legacy_rpg/main.py
```

Play through a fight or two. Save the game. Load it. Make sure you understand what every part does.

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
