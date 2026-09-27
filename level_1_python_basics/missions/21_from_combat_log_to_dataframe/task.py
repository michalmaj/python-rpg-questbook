# Mission 21: From Combat Log to DataFrame

import pandas as pd
from pathlib import Path

LOG_FILE = Path(__file__).parent / "sample_log.csv"
MESSY_FILE = Path(__file__).parent / "messy_log.csv"

# --- Load, then inspect ---
#
# TODO: Load LOG_FILE into a DataFrame, then look at what you loaded
# before calculating anything — call df.head(), df.shape, df.columns,
# df.dtypes, and df.info(). This is one habit, not five separate lessons.
df = None

# TODO: df.describe() returns a statistical summary (count, mean, std,
# min, max, ...) of every numeric column. Store it — the check uses it.
summary = None

# --- The three questions from Mission 20's game-design angle ---

# TODO: Calculate the average hero HP across all rounds.
avg_hero_hp = None

# TODO: Find the lowest hero HP recorded (the most dangerous moment).
min_hero_hp = None

# TODO: Find the round number when the boss reached 0 HP (the final round).
# Hint: filter with df[df["boss_hp"] == 0], then read the "round" column.
final_round = None

print("=== Combat Log ===")
print(f"Rounds fought:    {len(df) if df is not None else 'TODO'}")
print(f"Avg hero HP:      {avg_hero_hp}")
print(f"Lowest hero HP:   {min_hero_hp}")
print(f"Boss defeated on: round {final_round}")

# --- Notice: not every log is this clean ---
messy_df = pd.read_csv(MESSY_FILE)

# TODO: Which rows are missing hero_hp? .isna() on a column gives a
# boolean mask — the same idea as the masks from Mission 18, now on a
# DataFrame column instead of a NumPy array.
missing_hp = None

# TODO: How many rows are missing? (True counts as 1, same as before.)
missing_hp_count = None

# --- Decide ---
#
# A round with no recorded hero_hp doesn't tell us anything about hero
# survival, so for this analysis, dropping that row is the right call.
# That won't always be true — sometimes filling the gap (fillna) makes
# more sense, sometimes leaving it alone does. There's no single rule;
# you decide based on what the analysis needs.

# TODO: Remove the row(s) where hero_hp is missing.
clean_df = None

print()
print("=== Messy Log ===")
print(f"Missing hero_hp rows: {missing_hp_count}")
print(f"Rows after cleaning:  {len(clean_df) if clean_df is not None else 'TODO'}")
