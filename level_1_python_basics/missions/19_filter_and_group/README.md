# Mission 19: Filter and Group

## Goal

Add a calculated column, group heroes by class, filter winners, and rank by damage.

## You will learn

- `df["new_col"] = formula` — creating a calculated column
- `df.groupby("col")["col"].mean()` — aggregating groups
- `df[df["col"] == value]` — filtering rows by condition
- `df.sort_values("col", ascending=False)` — sorting
- `.iloc[0]` — selecting the first row after sorting

## Game problem

Ten heroes fought the Shadow Dragon. You have one row per hero: class, rounds survived, damage dealt, and whether they won. Questions a game designer asks:

- Which class deals the most damage on average?
- How many heroes survived?
- Who was the top damage dealer?

Pandas answers all three in four lines.

## Python concept

**Calculated column** — create a new column from existing ones:

```python
df["damage_per_round"] = df["damage_dealt"] / df["rounds_survived"]
```

Every row gets its own value automatically. No loop needed.

**groupby** — split into groups, apply a function, combine results:

```python
df.groupby("hero_class")["damage_dealt"].mean()
# hero_class
# Mage      132.0
# Rogue     139.0
# Warrior   155.0
```

**Filter** — keep only rows matching a condition:

```python
df[df["victory"] == 1]          # only winners
len(df[df["victory"] == 1])     # count of winners
```

**Sort and pick first** — rank and select the top entry:

```python
df.sort_values("damage_dealt", ascending=False).iloc[0]["hero_name"]
```

## Your task

Open `task.py`. Complete the four TODOs.

Expected output:
```
=== All Heroes ===
  hero_name hero_class  damage_dealt  damage_per_round  victory
0       Ada    Warrior           147             16.33        1
...

=== Avg Damage by Class ===
hero_class
Mage       132.0
Rogue      139.0
Warrior    155.0
Name: damage_dealt, dtype: float64

Victories:        6 / 10
Top damage hero:  Brom
```

## Run

```bash
uv run python missions/19_filter_and_group/task.py
```

## Check

```bash
uv run python missions/19_filter_and_group/check.py
```

## Side quest

Which class has the highest win rate? Combine groupby with victory:

```python
win_rate = df.groupby("hero_class")["victory"].mean()
print(win_rate)
```

This gives the fraction of wins per class (0.0 to 1.0). Which class is safest?

## Break it

Change `ascending=False` to `ascending=True` in TODO 4. The check fails because `iloc[0]` now returns the hero with the *lowest* damage. `sort_values` direction matters.

## Real-world translation

`groupby` is one of the most-used Pandas operations in data science. Whether grouping sales by region, errors by service, or players by rank — the pattern is always the same: split by category → compute per-group statistic → compare.

---

Next mission: `level_1_python_basics/missions/20_plot_the_results/README.md`
