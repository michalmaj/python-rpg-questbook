# Project 05: Game Analytics Report

## Final Boss — Part 2: Game Data Analysis

You built the game. Now answer real questions about it, using the combat
log and battle records from Missions 21 and 22.

## Questions

1. Which class deals the highest average damage?
2. How many battles dealt more than 150 damage?
3. What does the damage distribution look like — mean, spread, percentiles?
4. Which class has the highest win rate?
5. Who dealt the most damage of anyone in a single battle?
6. On which round is hero HP at its lowest?
7. What do a line chart of HP-over-time and a bar chart of damage-by-class
   look like for this data?

Each question below maps to one function in `analytics.py`. The check
calls these functions directly with its own data — the pandas/numpy calls
you use inside are your choice, but the function name, its inputs, and
what it returns are the contract the check relies on.

## Data

Two files, already read for you via `load_combat_log` / `load_battles`:

- **Combat log** (`round, hero_hp, boss_hp`) — one row per round of a single fight
- **Battles** (`hero_name, hero_class, damage_dealt, victory, ...`) — one row per hero across ten fights

## Tools you already have

Everything here is a direct application of Missions 17–23 — nothing new:

- Mission 18 gave you boolean masks (`arr[arr > x]`) — Question 2 is the same idea on a column.
- Mission 20 gave you `.mean()`, `.std()`, `np.percentile()` — Question 3 is those three, packaged into one dict.
- Mission 22 gave you `groupby`, filtering, and sorting — Questions 1, 4, and 5 are each one of those.
- Mission 23 gave you the `plt.plot` / `plt.bar` / `savefig` pattern — Question 7 is that, applied here.

## Check

```bash
uv run python projects/05_analytics_report/check.py
```

The check doesn't just run your script once and look at the printed
report — it imports your functions and calls each one with a small,
hand-checkable dataset built inside the check itself, separately from
the real game data. A function that only happens to work on the one
dataset you tested by eye won't pass.

## Run

```bash
uv run python projects/05_analytics_report/analytics.py
```

Then look at the charts:

```bash
open plots/report_hp.png
open plots/report_damage.png
```

## Challenge

Use your own Project 04 data instead — pass `M21_LOG`/`M22_LOG` a path to
your own `combat_log.csv`, or a battles CSV built from several of your
own runs, and see how your answers compare to the sample data.

---

You built a terminal RPG from scratch, then analyzed it with NumPy,
Pandas, and Matplotlib. That's Level 1 complete.
