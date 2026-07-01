# Mission 18: Read Combat Logs

## Goal

Load a CSV combat log into a Pandas DataFrame and extract key statistics.

## You will learn

- `import pandas as pd` — the convention for importing Pandas
- `pd.read_csv(filepath)` — loading a CSV file into a DataFrame
- `df.shape`, `df.columns` — inspecting a DataFrame
- `df["column"]` — selecting a single column
- `df["column"].mean()`, `.min()` — aggregating column values
- `df[df["column"] == value]` — filtering rows by condition

## Game problem

In Project 04 you wrote combat rounds to `combat_log.csv`. Now it's time to read that log and answer questions a game designer cares about:

- What was the average hero HP during the fight? (balance indicator)
- What was the most dangerous moment? (minimum hero HP)
- On which round did the boss die? (fight length)

## Python concept

A **DataFrame** is a table — rows and columns, like a spreadsheet, but in Python.

```python
import pandas as pd

df = pd.read_csv("sample_log.csv")
print(df.head())
#    round  hero_hp  boss_hp
# 0      1      106      133
# 1      2       92      116
# ...
```

Select a column and aggregate it:
```python
df["hero_hp"].mean()    # average HP across all rounds
df["hero_hp"].min()     # lowest HP (most dangerous moment)
```

Filter rows where a condition is true:
```python
df[df["boss_hp"] == 0]          # rows where boss is dead
df[df["boss_hp"] == 0]["round"] # just the round number
```

## Your task

Open `task.py`. Complete the four TODOs using `sample_log.csv` — a 9-round battle where the hero wins by a narrow margin.

Expected output:
```
   round  hero_hp  boss_hp
0      1      106      133
1      2       92      116
2      3       78       99
3      4       64       83
4      5       52       66
5      6       40       49
6      7       28       33
7      8       18       16
8      9       12        0

Rounds fought:    9
Avg hero HP:      54.4
Lowest hero HP:   12
Boss defeated on: round 9
```

## Run

```bash
uv run python missions/18_read_combat_logs/task.py
```

## Check

```bash
uv run python missions/18_read_combat_logs/check.py
```

## Side quest

Use your own combat log from Project 04. Copy it into this folder:

```bash
cp combat_log.csv missions/18_read_combat_logs/sample_log.csv
```

Run `task.py` again. The statistics will reflect your actual battle — every player's run looks different.

## Break it

Change `LOG_FILE` to point to a file that does not exist:

```python
LOG_FILE = Path(__file__).parent / "missing.csv"
```

Run `task.py`. You get `FileNotFoundError`. This is how Pandas reports a missing file — clear and specific.

## Real-world translation

`pd.read_csv()` is one of the most-used lines in all of data science. Whether it's sales records, sensor readings, or API logs — the workflow is always the same: read CSV → inspect shape and columns → aggregate and filter. You just did the whole workflow on game data.

---

Next mission: `level_1_python_basics/missions/19_filter_and_group/README.md`
