import pandas as pd
from pathlib import Path

LOG_FILE = Path(__file__).parent / "sample_log.csv"

# TODO: Load the CSV file into a DataFrame.
# Hint: pd.read_csv(filepath)
df = None  # replace None with pd.read_csv(LOG_FILE)

# TODO: Calculate the average hero HP across all rounds.
avg_hero_hp = None  # replace None with df["hero_hp"].mean()

# TODO: Find the lowest hero HP recorded (the most dangerous moment).
min_hero_hp = None  # replace None with df["hero_hp"].min()

# TODO: Find the round number when the boss reached 0 HP (the final round).
# Hint: use df[df["boss_hp"] == 0]["round"] to filter, then .values[0] to get the number
final_round = None  # replace None with df[df["boss_hp"] == 0]["round"].values[0]

if __name__ == "__main__":
    print(df)
    print()
    print(f"Rounds fought:    {len(df)}")
    print(f"Avg hero HP:      {avg_hero_hp:.1f}")
    print(f"Lowest hero HP:   {min_hero_hp}")
    print(f"Boss defeated on: round {final_round}")
