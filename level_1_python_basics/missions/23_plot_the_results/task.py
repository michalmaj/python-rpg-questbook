import matplotlib
matplotlib.use("Agg")  # save to file without needing a display
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

M21_LOG = Path(__file__).parents[1] / "21_from_combat_log_to_dataframe" / "sample_log.csv"
M22_LOG = Path(__file__).parents[1] / "22_filter_group_rank" / "battles_log.csv"
PLOTS_DIR = Path(__file__).parents[2] / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

combat_df = pd.read_csv(M21_LOG)
battles_df = pd.read_csv(M22_LOG)
avg_damage = battles_df.groupby("hero_class")["damage_dealt"].mean()

# --- Chart 1: HP over time ---
#
# TODO: Plot combat_df["hero_hp"] and combat_df["boss_hp"] against
# combat_df["round"] as two lines on the same chart. Add a title, axis
# labels, and a legend so the lines are distinguishable. Save the result
# to PLOTS_DIR / "hp_chart.png", then close the figure.


# --- Chart 2: Average damage by class ---
#
# TODO: Start a new figure (plt.figure()), then draw a bar chart of
# avg_damage — its index on the x-axis, its values as bar heights. Add a
# title and axis labels. Save to PLOTS_DIR / "damage_chart.png", then close.


print(f"Charts saved to: {PLOTS_DIR}")
