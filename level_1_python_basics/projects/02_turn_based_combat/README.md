# Project 02: Turn-Based Combat Arena

## Boss Fight — World 2: Combat Logic

You practiced the `while` loop, the `for` loop, and lists across three missions. Now put them together in one arena.

| Skill | Mission |
|-------|---------|
| `while` loop | Mission 04: Combat Loop |
| `for` loop, `range()` | Mission 05: Arena Challenge |
| lists, `append`, `len`, `pop` | Mission 06: Hero Inventory |

## What you build

A combat simulation that runs three back-to-back arena fights:

1. A `for` loop runs through a list of enemies, one at a time
2. A `while` loop inside handles each fight, round by round
3. A `potions` list tracks the hero's inventory — `pop()` removes a potion when used
4. A `battle_log` list collects results — `append()` adds one string per fight
5. A final `for` loop prints the battle summary

## Files

| File | Your role |
|------|-----------|
| `task.py` | Edit — all TODOs are in here |
| `check.py` | Run to verify |

## Your tasks

Open `task.py`. The structure is already there. Your job is to complete the combat logic inside the `while` loop:

**Step 1** — Hero attacks: subtract `hero_attack` from `enemy_hp`. If `enemy_hp` drops to 0 or below, set it to 0, print the defeat message, append to `battle_log`, and `break`.

**Step 2** — Enemy attacks back: subtract `enemy_attack` from `hero_hp`. If `hero_hp` drops to 0 or below, set it to 0.

**Step 3** — Healing: if `hero_hp < 40` and `len(potions) > 0`, call `potions.pop()` to remove the last potion, add the heal to `hero_hp`, and print the potion message.

**Step 4** — After the `for` loop ends, print whether the hero won or fell, then loop over `battle_log` and print each entry.

## Run

```bash
uv run python projects/02_turn_based_combat/task.py
```

Expected output (values depend on your stats):

```
=== Ada enters the Arena ===
Potions: 3

--- Wolf appears! (HP: 30, Attack: 8) ---
  Round 1: Hero HP: 92. Wolf HP: 10
  Round 2: Wolf falls!

--- Orc Warrior appears! (HP: 55, Attack: 13) ---
  ...

Ada wins the arena!

--- Battle Summary ---
  Defeated Wolf in 2 rounds
  Defeated Orc Warrior in 3 rounds
  Defeated Dragon King in 5 rounds

Hero HP remaining: 46
Potions remaining: 1
```

## Check

```bash
uv run python projects/02_turn_based_combat/check.py
```

## Try it yourself

1. Increase `Dragon King` HP to 150. Does the hero survive without extra potions?
2. Add a fourth enemy — `"Ancient Lich"` with 120 HP and 25 attack. Adjust potions accordingly.
3. Change the potion trigger from `hero_hp < 40` to `hero_hp < 20`. How does the fight change?

## Break it

Empty the `potions` list (`potions = []`). Run the arena again. The hero has no healing — do they still win? Which enemy kills them first?

## Real-world translation

A `for` loop that contains a `while` loop is the standard pattern for "process each item until a condition is met" — database row processing, retry loops over API calls, game state machines. The `battle_log` list is the same pattern as an event log or audit trail: append during the operation, display at the end.

---

*World 2 clear. Next: `level_1_python_basics/missions/07_monster_dictionary/README.md`*
