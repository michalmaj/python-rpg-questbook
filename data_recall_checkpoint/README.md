# Data Recall Checkpoint: Combat Log Analytics

You learned NumPy and Pandas back in Level 1. Since then the RPG has gained
validation (Pydantic) and persistence (the repository pattern) in Level 3 —
including a real, validated combat log. Before moving into Level 4's
interfaces and tooling, use those data skills again on the combat logs your
application now knows how to store.

This is **recall, not a new lesson**. No new concepts. No new library.
30–60 minutes.

## The model

Level 3 Mission 06 introduced `CombatLogRow`: one row per **turn**, not per
battle. A single battle (`battle_id`) usually spans several rows — all but
the last have `result == "ongoing"`; only the final row of a battle has a
terminal `result` (`"win"` or `"loss"`). To compute a win rate you need
exactly the terminal rows, not every row.

## The data

`data/combat_log_fixture.csv` — ~220 rows, same schema `CsvCombatLogRepository`
writes:

```
battle_id, turn, hero_name, hero_class, monster, action,
damage_dealt, damage_taken, hero_hp, monster_hp, result
```

`action` is `"attack"` or `"potion"`. `result` is `"ongoing"`, `"win"`, or
`"loss"`. You don't need to generate this data yourself — it's provided so
grading is stable regardless of how much you've personally played.

A second file, `combat_log_fixture_variant.csv`, has the same shape but
different numbers (including a different monster difficulty ranking) — the
checker uses it to make sure your answers actually come from the data, not
from a number you typed once and left there.

## Cheat-sheet (you've seen all of this in Level 1)

```python
df = pd.read_csv(path)                          # M21
df[df["col"] != "x"]                             # M22 — filter
df.groupby("col")["other"].apply(fn)             # M22 — groupby
df.sort_values("col")                            # M22 — sort/rank
arr = df["col"].to_numpy()                        # M17 — array
arr.mean(), arr.std(), np.percentile(arr, 75)    # M20 — aggregations
arr > threshold                                   # M18 — boolean mask
```

Relevant Level 1 missions if you want a refresher: [17 — Dice Become Arrays](../level_1_python_basics/missions/17_dice_become_arrays/README.md), [18 — Critical Hits](../level_1_python_basics/missions/18_critical_hits/README.md), [20 — Damage Distributions](../level_1_python_basics/missions/20_damage_distributions/README.md), [21 — From Combat Log to DataFrame](../level_1_python_basics/missions/21_from_combat_log_to_dataframe/README.md), [22 — Filter, Group, Rank](../level_1_python_basics/missions/22_filter_group_rank/README.md).

## Your task

Open `task.py` and implement all four functions.

```python
def load_combat_log(path: Path) -> pd.DataFrame: ...
def win_rate_by_class(df: pd.DataFrame) -> dict[str, float]: ...
def damage_stats(df: pd.DataFrame) -> dict[str, float | int]: ...
def rank_monsters_by_difficulty(df: pd.DataFrame) -> list[str]: ...
```

Each function's docstring has the exact contract. Two notes worth reading
before you start:

- **`win_rate_by_class` must use pandas' `groupby`.** A per-class Python
  loop can produce the same numbers, but `groupby` is specifically what
  this task is here to reactivate — the checker looks for it.
- **`damage_stats` only counts `"attack"` rows.** A `"potion"` turn has
  `damage_dealt == 0` because the hero healed instead of attacking, not
  because the hit was weak — mixing those zeros into the stats would
  understate real attack damage.

## Questions this answers

- Which hero class wins most often, and by how much?
- What does a "hard-hitting" attack look like in this log (p75), and how
  often does one land?
- Which monster is operationally the hardest, by this log's win rates alone?

## How to check

```bash
uv run python data_recall_checkpoint/check.py
```

The checker runs every function against two different fixtures and checks
the actual values — not your code's syntax. It also confirms `groupby` is
really used in `win_rate_by_class` and that `np.percentile` is really called
in `damage_stats`, since those two specific APIs are the point of this
checkpoint.

---

**Next:** [Level 4 — Interfaces and Reports](../level_4_interfaces/README.md)
