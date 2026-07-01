# Mission 17: Damage Distributions

## Goal

Compare two weapons with the same average damage using standard deviation and percentiles.

## You will learn

- `array.std()` — standard deviation: how spread out the values are
- `np.percentile(array, q)` — what damage value sits at the q-th percentile
- Why average alone is not enough to describe a weapon

## Game problem

The Warrior and the Rogue both deal average 3.5 damage:
- Warrior rolls a d6: values 1, 2, 3, 4, 5, 6
- Rogue rolls a d4+1: values 2, 3, 4, 5

Same average. But in a long fight, they behave very differently. How do you measure that difference?

## Python concept

**Standard deviation** (`std`) measures spread. A high std means rolls vary a lot; a low std means they cluster near the average.

```python
import numpy as np

warrior = np.random.randint(1, 7, size=10000)   # d6
rogue   = np.random.randint(2, 6, size=10000)   # d4+1

print(warrior.std())   # ≈ 1.71 — wide spread
print(rogue.std())     # ≈ 1.12 — tighter spread
```

**Percentile** answers: "What damage do I deal in my worst 25% of rolls?"

```python
np.percentile(warrior, 25)   # ≈ 2.0 — 25% of rolls land at 2 or below
np.percentile(warrior, 75)   # ≈ 5.0 — 75% of rolls land at 5 or below
```

The gap between p25 and p75 (the **interquartile range**) tells you how consistent your damage is.

## Your task

Open `task.py`. Complete the six TODOs:

1. `warrior_mean` — mean of warrior_rolls
2. `rogue_mean` — mean of rogue_rolls
3. `warrior_std` — std of warrior_rolls
4. `rogue_std` — std of rogue_rolls
5. `warrior_p25` — 25th percentile of warrior_rolls
6. `warrior_p75` — 75th percentile of warrior_rolls

Expected output (values vary slightly each run):
```
=== Warrior (d6: 1–6) ===
Mean:     3.50
Std dev:  1.71
25th pct: 2.0
75th pct: 5.0

=== Rogue (d4+1: 2–5) ===
Mean:     3.50
Std dev:  1.12

Same average, different spread — which do you prefer?
```

## Run

```bash
uv run python missions/17_damage_distributions/task.py
```

## Check

```bash
uv run python missions/17_damage_distributions/check.py
```

## Side quest

The check verifies that `warrior_std > rogue_std`. Think about game design:

- A **high-std weapon** (Warrior d6) is exciting but unreliable — you might one-shot a boss or deal 1 damage.
- A **low-std weapon** (Rogue d4+1) is consistent — steady damage every round, easier to plan around.

Try computing `np.percentile(warrior_rolls, 10)` — the "10th percentile" damage. That's what you deal in your worst 10% of rounds. A Warrior's worst 10% is often just 1 damage. A Rogue's worst 10% is 2. Which matters more in a tight fight?

## Break it

Change `size=10000` to `size=1`. Rerun the check — the std assertion will fail because a single roll has `std=0`. With one data point, there is no spread. This is why you need many samples for statistics to be meaningful.

## Real-world translation

This exact workflow — mean, std, percentiles — is used everywhere data matters: A/B tests measure if one version is significantly better than another; finance compares asset volatility; operations monitors server response times at the 99th percentile.

---

Next mission: `level_1_python_basics/missions/18_read_combat_logs/README.md`
