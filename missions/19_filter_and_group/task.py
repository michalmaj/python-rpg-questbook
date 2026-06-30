import pandas as pd
from pathlib import Path

LOG_FILE = Path(__file__).parent / "battles_log.csv"
df = pd.read_csv(LOG_FILE)

# TODO 1: Add a new column "damage_per_round" = damage_dealt ÷ rounds_survived.
# In Pandas you create a column by assigning to df["new_column_name"].
df["damage_per_round"] = None  # replace None with: df["damage_dealt"] / df["rounds_survived"]

# TODO 2: Group by hero_class and calculate the mean damage_dealt per class.
# Hint: df.groupby("column")["column"].mean()
avg_damage_by_class = None

# TODO 3: Count how many heroes won (victory == 1).
# Hint: filter with df[df["victory"] == 1], then use len()
victory_count = None

# TODO 4: Find the name of the hero who dealt the most total damage.
# Hint: df.sort_values("damage_dealt", ascending=False).iloc[0]["hero_name"]
top_damage_hero = None

if __name__ == "__main__":
    print("=== All Heroes ===")
    print(df[["hero_name", "hero_class", "damage_dealt", "damage_per_round", "victory"]])
    print()
    print("=== Avg Damage by Class ===")
    print(avg_damage_by_class)
    print()
    print(f"Victories:        {victory_count} / {len(df)}")
    print(f"Top damage hero:  {top_damage_hero}")
