import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
M18_LOG = REPO_ROOT / "missions" / "18_read_combat_logs" / "sample_log.csv"
M19_LOG = REPO_ROOT / "missions" / "19_filter_and_group" / "battles_log.csv"
PLOTS_DIR = REPO_ROOT / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

# ── Section 1: Combat Log (Pandas) ──────────────────────────────────────────
# TODO: Load M18_LOG into a DataFrame called combat_df.
combat_df = None

# TODO: Compute these three values from combat_df:
#   avg_hero_hp  — mean of the "hero_hp" column
#   min_hero_hp  — minimum of the "hero_hp" column
#   final_round  — round number where boss_hp == 0
avg_hero_hp = None
min_hero_hp = None
final_round = None

# ── Section 2: Damage Distributions (NumPy) ─────────────────────────────────
warrior_rolls = np.random.randint(1, 7, size=10000)   # d6
rogue_rolls   = np.random.randint(2, 6, size=10000)   # d4+1

# TODO: Compute warrior statistics: mean, std, 25th and 75th percentile.
warrior_mean = None
warrior_std  = None
warrior_p25  = None
warrior_p75  = None

# TODO: Compute rogue statistics: mean and std.
rogue_mean = None
rogue_std  = None

# ── Section 3: Hero Class Comparison (Pandas groupby) ───────────────────────
# TODO: Load M19_LOG into battles_df.
battles_df = None

# TODO: Group by "hero_class", compute mean of "damage_dealt".
avg_damage_by_class = None

# TODO: Count how many heroes won (victory == 1).
victory_count = None

# ── Section 4: Charts (Matplotlib) ──────────────────────────────────────────
# TODO: Chart 1 — line chart of hero_hp and boss_hp over rounds.
#   - Two lines: one for "Hero HP", one for "Boss HP"
#   - Title: "Combat: HP per Round"
#   - Labels and legend
#   - Save to PLOTS_DIR / "report_hp.png", then close.

# TODO: Chart 2 — bar chart of avg_damage_by_class.
#   - plt.figure() to start fresh
#   - Title: "Average Damage by Hero Class"
#   - Save to PLOTS_DIR / "report_damage.png", then close.

# ── Print Report ─────────────────────────────────────────────────────────────
print("=" * 50)
print("  GAME ANALYTICS REPORT")
print("=" * 50)

print(f"\nCombat rounds:   {len(combat_df)}")
print(f"Avg hero HP:     {avg_hero_hp:.1f}")
print(f"Lowest hero HP:  {min_hero_hp}")
print(f"Boss defeated:   round {final_round}")

print(f"\nWarrior d6  — mean: {warrior_mean:.2f}  std: {warrior_std:.2f}  p25–p75: {warrior_p25}–{warrior_p75}")
print(f"Rogue d4+1  — mean: {rogue_mean:.2f}  std: {rogue_std:.2f}")

print(f"\nAvg damage by class:\n{avg_damage_by_class.to_string()}")
print(f"\nVictories: {victory_count} / {len(battles_df)}")

print(f"\nCharts saved to: {PLOTS_DIR}")
print("\n" + "=" * 50)
print("  REPORT COMPLETE")
print("=" * 50)
