# Project 05: Game Analytics Report

## Final Boss — Part 2: Game Data Analysis

This is the last project. You built the game. Now you analyze it.

Everything from Part 2 comes together in one script:

| Skill | Mission |
|-------|---------|
| pd.read_csv, DataFrame | Mission 18 |
| groupby, filter, sort  | Mission 19 |
| np.random, mean, std   | Mission 16–17 |
| plt.plot, plt.bar      | Mission 20 |

## What you build

A single script (`analytics.py`) that:

1. Loads the combat log → computes average and minimum hero HP, finds the final round
2. Simulates 10 000 damage rolls per weapon → compares Warrior vs Rogue with std and percentiles
3. Loads the battles log → groups heroes by class, counts victories
4. Saves two charts to the `plots/` folder
5. Prints a structured report

## Files

| File | Your role |
|------|-----------|
| `analytics.py` | Edit — 4 sections of TODOs |
| `check.py` | Run to verify |

Data files live in their respective mission folders (`level_1_python_basics/missions/18_…` and `level_1_python_basics/missions/19_…`) — no copying needed.

## Your tasks

Open `analytics.py`. Work through the four sections in order — each builds on the previous.

**Section 1** — Load `M18_LOG` into `combat_df`. Compute `avg_hero_hp`, `min_hero_hp`, `final_round`.

**Section 2** — Compute NumPy statistics for `warrior_rolls` and `rogue_rolls` (mean, std, percentiles).

**Section 3** — Load `M19_LOG` into `battles_df`. Group by class for `avg_damage_by_class`. Count `victory_count`.

**Section 4** — Create two charts (HP line chart → `report_hp.png`, damage bar chart → `report_damage.png`).

All TODOs must be complete before the print section at the bottom will run.

## Run

```bash
uv run python projects/05_analytics_report/analytics.py
```

Expected output:
```
==================================================
  GAME ANALYTICS REPORT
==================================================

Combat rounds:   9
Avg hero HP:     54.4
Lowest hero HP:  12
Boss defeated:   round 9

Warrior d6  — mean: 3.50  std: 1.71  p25–p75: 2.0–5.0
Rogue d4+1  — mean: 3.50  std: 1.12

Avg damage by class:
hero_class
Mage       132.0
Rogue      139.0
Warrior    155.0

Victories: 6 / 10

Charts saved to: /path/to/plots

==================================================
  REPORT COMPLETE
==================================================
```

Then open the charts:

```bash
open plots/report_hp.png
open plots/report_damage.png
```

## Check

```bash
uv run python projects/05_analytics_report/check.py
```

## Challenge

Use your own Project 04 data. Replace `M18_LOG` with the root-level `combat_log.csv` and `M19_LOG` with a battles log of your own runs. Run the game several times with different hero classes, collect the rows manually, and see how your real stats compare to the sample data.

---

*You built a terminal RPG from scratch. You analyzed it with NumPy, Pandas, and Matplotlib. That is a complete data-driven Python project — the same stack used in production data science every day.*
