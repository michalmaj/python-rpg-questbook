# Mission 23: Plot the Results

## Goal

Turn DataFrame columns into saved chart images — a line chart and a bar
chart.

## Game problem

Numbers in a table are hard to read at a glance. A line chart of HP over
time shows instantly when a fight was close. A bar chart of damage by
class shows instantly which class hits harder.

## Python concept

Matplotlib follows a state-machine model — each call modifies the current
figure, until you save and close it.

```python
import matplotlib
matplotlib.use("Agg")   # must come BEFORE importing pyplot
import matplotlib.pyplot as plt

quests = [1, 2, 3, 4, 5]
gold_collected = [50, 80, 65, 120, 95]

plt.plot(quests, gold_collected, label="Gold")
plt.title("Gold per Quest")
plt.xlabel("Quest")
plt.ylabel("Gold")
plt.legend()
plt.savefig("gold_chart.png")
plt.close()             # always close before starting a new chart
```

A bar chart follows the same pattern with `plt.bar` instead of `plt.plot`:

```python
spell_schools = ["Fire", "Ice", "Shock"]
avg_mana_cost = [35, 28, 42]

plt.bar(spell_schools, avg_mana_cost)
plt.title("Average Mana Cost by School")
plt.xlabel("School")
plt.ylabel("Mana")
plt.savefig("mana_chart.png")
plt.close()
```

`matplotlib.use("Agg")` switches to a file-only backend. Without it,
Matplotlib tries to open a window — which fails in terminals without a
display (WSL, SSH, CI).

## Your task

Open `task.py`. The data is already loaded: `combat_df` (round, hero_hp,
boss_hp) and `avg_damage` (mean damage_dealt per hero_class). Apply the
pattern above to them:

**Chart 1** — line chart of `hero_hp` and `boss_hp` against `round`,
saved to `hp_chart.png`.

**Chart 2** — bar chart of `avg_damage`, saved to `damage_chart.png`.

## Run

```bash
uv run python missions/23_plot_the_results/task.py
```

```bash
open plots/hp_chart.png      # macOS
xdg-open plots/hp_chart.png  # Linux
```

## Check

```bash
uv run python missions/23_plot_the_results/check.py
```

The check confirms the charts actually plot `combat_df` and `avg_damage`
— not just that two PNG files happen to exist.

## Side quest

Use your own Project 04 combat log for Chart 1:

```python
# In task.py, change M21_LOG to point to the root-level combat_log.csv
M21_LOG = Path(__file__).parents[2] / "combat_log.csv"
```

## Break it

Skip `plt.close()` between the two charts. Both datasets get drawn onto
the same figure — lines and bars tangled together. `plt.close()` is how
you tell Matplotlib "start fresh."

---

Course complete! Final boss: `level_1_python_basics/projects/05_analytics_report/README.md`
