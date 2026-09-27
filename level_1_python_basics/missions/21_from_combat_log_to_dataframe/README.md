# Mission 21: From Combat Log to DataFrame

## Goal

Load a combat log into a DataFrame, get in the habit of looking at data
before analyzing it, and handle a small gap in that data on purpose.

## Game problem

You've already worked with this shape of data twice:

```python
combat_log = [
    {"round": 1, "hero_hp": 90, "boss_hp": 140},
    {"round": 2, "hero_hp": 71, "boss_hp": 118},
]
```

In Mission 12 you built a list of dicts like this. In Project 04 you saved
it as a CSV — one row per dict, one column per key. A list of dicts is a
collection of records; a CSV is the same records written as a table. A
DataFrame isn't a different kind of data — it's a tool built for working
with that table: filtering, per-column stats, grouping, all without a loop.

## Your task — four steps

**Load.** Read `sample_log.csv` into a DataFrame.

**Inspect.** Before calculating anything, look at what you loaded —
`df.head()`, `df.shape`, `df.columns`, `df.dtypes`, `df.info()`. That's
one habit, not five separate lessons: run all of them, read the output,
move on. `df.describe()` goes a step further — a statistical summary
(count, mean, std, min, max, ...) of every numeric column. Store its
result; the check uses it.

Every column has a `dtype` — `df.dtypes` tells you whether a column holds
numbers or text. You don't need the details of Pandas's type system yet;
just notice that types exist, and that Pandas already got them right when
it read the CSV.

**Notice.** Open `messy_log.csv` — same idea, but one round's `hero_hp`
was never recorded. Find which row, and count how many rows are affected.

**Decide.** A round with no recorded HP can't tell you anything about
hero survival, so for this analysis, dropping that row is the right call.
That won't always be true — sometimes filling the gap (`fillna`) makes
more sense, sometimes leaving it alone does. There's no single correct
rule; you decide based on what the analysis needs.

Worth knowing: many Pandas aggregations (`.mean()`, `.sum()`, ...) already
skip `NaN` on their own. Dropping rows isn't something Pandas forces on
you — it's a choice you make for a reason.

## Missing values, technically

A missing value shows up as `NaN` (not a number). `.isna()` on a column
gives you a `True`/`False` Series — the same boolean-mask idea from
Mission 18, now applied to a DataFrame column instead of an array:

```python
inventory_value = pd.Series([50, None, 30, None])
inventory_value.isna()
# 0    False
# 1     True
# 2    False
# 3     True
# dtype: bool

inventory_value.isna().sum()   # 2 — how many are missing
inventory_value.dropna()        # keep only the non-missing ones
```

Not every gap should be dropped, though — it depends what the missing
value *means*. If the missing column had been `bonus_damage` instead of
`hero_hp`, a blank cell might reasonably mean "no bonus applied," and
filling it in would keep the row instead of throwing it away:

```python
bonus_damage = pd.Series([5, None, 10, None])
bonus_damage.fillna(0)
# 0     5.0
# 1     0.0
# 2    10.0
# 3     0.0
# dtype: float64
```

Same mechanic, opposite decision. `dropna()` was right for `hero_hp`
because a round you can't measure isn't useful data. `fillna(0)` would be
right for `bonus_damage` because "nothing recorded" and "zero bonus" mean
the same thing there. The column's meaning decides the tool, not the
other way around.

## Run

```bash
uv run python missions/21_from_combat_log_to_dataframe/task.py
```

## Check

```bash
uv run python missions/21_from_combat_log_to_dataframe/check.py
```

## Side quest

Use your own combat log from Project 04:

```bash
cp combat_log.csv missions/21_from_combat_log_to_dataframe/sample_log.csv
```

Run `task.py` again — the statistics reflect your actual battle.

---

Next mission: `level_1_python_basics/missions/22_filter_group_rank/README.md`
