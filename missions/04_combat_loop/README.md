# Mission 04: Combat Loop

## Goal

Make the hero and a monster fight each other, round by round, until one of them falls.

## You will learn

- `while` — repeat a block as long as a condition is true
- Updating a variable inside a loop (`round_number += 1`)
- Combining a loop with `max()` and `min()` from Mission 02

## Game problem

So far the hero can take a single hit. Real combat takes many rounds.
We need a loop that keeps running until someone's HP reaches 0.

## Your task

Open `task.py`. The hero and monster stats are already set.
Write a `while` loop and a final summary.

**Step 1 — the loop:**

```python
while hero_hp > 0 and monster_hp > 0:
    round_number += 1
    monster_hp = max(0, monster_hp - hero_damage)
    hero_hp = max(0, hero_hp - monster_damage)
    print(f"Round {round_number}: Hero {hero_hp} HP | {monster_name} {monster_hp} HP")
```

**Step 2 — the summary (after the loop):**

```python
if hero_hp > 0:
    print(f"Hero wins in {round_number} rounds!")
else:
    print(f"{monster_name} wins in {round_number} rounds!")
```

> **Tip:** If `check.py` seems frozen, press **Ctrl+C** — your loop may be running forever.
> Make sure `hero_hp` and `monster_hp` both decrease inside the loop.

## Run

```bash
uv run python missions/04_combat_loop/task.py
```

Expected output:
```
=== Battle Begins! ===
Hero:    100 HP
Goblin: 60 HP

Round 1: Hero 88 HP | Goblin 45 HP
Round 2: Hero 76 HP | Goblin 30 HP
Round 3: Hero 64 HP | Goblin 15 HP
Round 4: Hero 52 HP | Goblin 0 HP
=== Battle Over ===
Hero wins in 4 rounds!
```

## Check

```bash
uv run python missions/04_combat_loop/check.py
```

## Side quest

Change `monster_damage` to `30`. How many rounds does the hero survive?
Who wins? What changes in the summary?

Try making the monster tougher: `monster_hp = 200`. Does the hero stand a chance?

---

Next mission: `missions/05_arena_challenge/README.md`
