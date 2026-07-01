# Mission 05: Arena Challenge

## Goal

Run a battle for exactly five rounds — no matter what happens.

## You will learn

- `for` loop — repeat a block a known number of times
- `range(n)` and `range(start, stop)` — generate a sequence of numbers
- When to use `for` instead of `while`

## Game problem

In Mission 04 the battle ran *until someone fell* — we didn't know how many rounds that would take.
Now the arena has a rule: **exactly 5 rounds**, then time is called.
When the count is fixed, `for` is the right tool.

## Your task

Open `task.py`. Write the loop and the final summary.

**`for` loop reminder:**

```python
for round_number in range(1, rounds + 1):
    # round_number is 1, 2, 3, 4, 5
    ...
```

`range(1, 6)` produces `1 2 3 4 5` — start is included, stop is excluded.
`range(5)` produces `0 1 2 3 4` — useful when you don't need a human-readable counter.

**Step 1 — the loop:**

```python
for round_number in range(1, rounds + 1):
    enemy_hp = max(0, enemy_hp - hero_damage)
    hero_hp = max(0, hero_hp - enemy_damage)
    print(f"Round {round_number}: Hero {hero_hp} HP | {enemy_name} {enemy_hp} HP")
```

**Step 2 — the summary (after the loop):**

```python
if hero_hp > 0:
    print(f"Hero survives with {hero_hp} HP!")
else:
    print("Hero has fallen.")
```

## Run

```bash
uv run python missions/05_arena_challenge/task.py
```

Expected output:
```
=== Arena Challenge: 5 Rounds ===
Hero:         100 HP
Stone Golem: 200 HP

Round 1: Hero 88 HP | Stone Golem 185 HP
Round 2: Hero 76 HP | Stone Golem 170 HP
Round 3: Hero 64 HP | Stone Golem 155 HP
Round 4: Hero 52 HP | Stone Golem 140 HP
Round 5: Hero 40 HP | Stone Golem 125 HP

=== Time is up! ===
Hero survives with 40 HP!
```

## Check

```bash
uv run python missions/05_arena_challenge/check.py
```

## Side quest

Change `rounds` to `10`. Does the hero survive all 10 rounds?

Then try `enemy_damage = 15`. How many rounds until the hero falls?
Switch back to `while` from Mission 04 — which loop fits better for each question?

---

Next mission: `level_1_python_basics/missions/06_hero_inventory/README.md`
