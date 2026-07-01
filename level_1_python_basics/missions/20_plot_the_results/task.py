import matplotlib
matplotlib.use("Agg")  # save to file without needing a display
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

M18_LOG = Path(__file__).parents[1] / "18_read_combat_logs" / "sample_log.csv"
M19_LOG = Path(__file__).parents[1] / "19_filter_and_group" / "battles_log.csv"
PLOTS_DIR = Path(__file__).parents[2] / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

combat_df = pd.read_csv(M18_LOG)
battles_df = pd.read_csv(M19_LOG)
avg_damage = battles_df.groupby("hero_class")["damage_dealt"].mean()

# --- Chart 1: HP over time ---

# TODO: Plot hero HP and boss HP as two lines over the combat rounds.
# plt.plot(combat_df["round"], combat_df["hero_hp"], label="Hero HP")
# plt.plot(combat_df["round"], combat_df["boss_hp"], label="Boss HP")

# TODO: Add a title and axis labels.
# plt.title("Combat: HP per Round")
# plt.xlabel("Round")
# plt.ylabel("HP")

# TODO: Add a legend so readers know which line is which.
# plt.legend()

# TODO: Save the chart and close it.
# plt.savefig(PLOTS_DIR / "hp_chart.png")
# plt.close()

# --- Chart 2: Average damage by class ---

# TODO: Start a new figure, then plot a bar chart of avg_damage.
# plt.figure()
# plt.bar(avg_damage.index, avg_damage.values)
# plt.title("Average Damage Dealt by Hero Class")
# plt.xlabel("Class")
# plt.ylabel("Avg Damage")
# plt.savefig(PLOTS_DIR / "damage_chart.png")
# plt.close()

print(f"Charts saved to: {PLOTS_DIR}")
