# Project 02: Turn-Based Combat Arena

## Boss Fight — World 2: Combat Logic

You practiced the `while` loop, the `for` loop, and lists across three missions. Now put them together in one arena.

| Skill | Mission |
|-------|---------|
| `while` loop | Mission 04: Combat Loop |
| `for` loop, `range()` | Mission 05: Arena Challenge |
| lists, `append`, `len`, `pop` | Mission 06: Hero Inventory |

## What you build

A combat simulation that runs three back-to-back arena fights, structured
around two functions:

- `fight_enemy(...)` — one fight, round by round, until someone's HP hits 0
- `run_arena(...)` — sends the hero through every enemy in sequence, using `fight_enemy`

This split isn't just style: `check.py` calls `fight_enemy` directly with
its own test numbers, so your combat rule gets tested on more than just
the one hardcoded run.

## Files

| File | Your role |
|------|-----------|
| `task.py` | Edit — the TODOs are inside `fight_enemy` |
| `check.py` | Run to verify |

## Your task

Open `task.py`. `run_arena` and the module-level setup are already wired
up and call `fight_enemy` for you — your job is everything *inside*
`fight_enemy`'s `while` loop:

1. **Hero attacks** — subtract `hero_attack` from `enemy_hp` (floor at 0).
   If the enemy is now dead, `break` immediately — no retaliation this round.
2. **Enemy attacks back** — subtract `enemy_attack` from `hero_hp` (floor at 0).
3. **Heal or report** — if `hero_hp` is below `heal_threshold` and there
   are potions left, pop one and add its value to `hero_hp`. Otherwise,
   print the round status.

`fight_enemy` returns `(hero_hp, rounds, hero_won)` — that's the contract
`run_arena` (and the check) relies on.

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
