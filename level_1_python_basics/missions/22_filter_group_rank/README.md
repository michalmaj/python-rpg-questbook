# Mission 22: Filter, Group, Rank

## Goal

Add a calculated column, group heroes by class, filter by a condition, and
rank them by damage — the same DataFrame, five different questions.

## Game problem

Ten heroes fought the Shadow Dragon. You have one row per hero: class,
rounds survived, damage dealt, whether they won. A game designer asks:

- Which class deals the most damage on average?
- How many heroes survived?
- Who was the top damage dealer?
- Who dealt serious damage — well above the pack?

## Python concept

**Calculated column** — build a new column from existing ones:

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

**Sort and pick first** — rank and select the top entry:

```python
df.sort_values("damage_dealt", ascending=False).iloc[0]["hero_name"]
```

## Filtering is the same mask you already know

In Mission 18 you filtered a NumPy array with a boolean mask:

```python
rolls[rolls > 4]
```

Filtering a DataFrame works exactly the same way — a condition, a mask, an
index:

```python
df["damage_dealt"] > 150     # a Series of True/False, one per row
df[df["damage_dealt"] > 150] # only the rows where that's True
```

`df["damage_dealt"] > 150` builds the mask. Wrapping it in `df[...]` uses
it to select matching rows — same idea as `arr[mask]`, applied to a table
instead of an array.

## One column vs. several

`df["damage_dealt"]` (single brackets) selects one column — a **Series**.
`df[["hero_name", "damage_dealt"]]` (a list of names, so double brackets)
selects several columns at once — a **DataFrame**, even if it only has two
columns. The double-bracket version is what you'll reach for whenever you
need more than one column together.

## Your task

Open `task.py`. Complete the six TODOs.

## Run

```bash
uv run python missions/22_filter_group_rank/task.py
```

## Check

```bash
uv run python missions/22_filter_group_rank/check.py
```

## Side quest

Combining two conditions needs `&` and parentheses around each side —
same rule as on NumPy arrays, never Python's `and`:

```python
df[(df["hero_class"] == "Warrior") & (df["victory"] == 1)]
```

Which class has the highest win rate?

```python
df.groupby("hero_class")["victory"].mean()
```

Neither is required to complete the mission.

## Break it

Change `ascending=False` to `ascending=True` in TODO 4. The check fails
because `iloc[0]` now returns the hero with the *lowest* damage —
`sort_values` direction matters.

---

Next mission: `level_1_python_basics/missions/23_plot_the_results/README.md`
