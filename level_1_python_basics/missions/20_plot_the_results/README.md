# Mission 20: Plot the Results

## Goal

Turn the combat log and battle stats into two charts saved as PNG files.

## You will learn

- `import matplotlib.pyplot as plt` — the plotting library
- `matplotlib.use("Agg")` — headless backend (saves to file, no window needed)
- `plt.plot(x, y, label="...")` — line chart
- `plt.bar(x, height)` — bar chart
- `plt.title()`, `plt.xlabel()`, `plt.ylabel()`, `plt.legend()` — labels
- `plt.savefig(path)` — save chart to a file
- `plt.close()` — close a figure before starting the next one

## Game problem

Numbers in a table are hard to read. A line chart of HP over time shows instantly when the fight was close. A bar chart of damage by class shows instantly which class hits harder. One glance beats ten lines of `print()`.

## Python concept

Matplotlib follows a **state machine** model — each function call modifies the current figure:

```python
import matplotlib
matplotlib.use("Agg")   # must come BEFORE importing pyplot
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [100, 80, 60], label="Hero HP")
plt.plot([1, 2, 3], [150, 130, 110], label="Boss HP")
plt.title("HP over Time")
plt.xlabel("Round")
plt.ylabel("HP")
plt.legend()
plt.savefig("chart.png")
plt.close()             # always close before starting a new chart
```

`matplotlib.use("Agg")` switches to a file-only backend. Without it, Matplotlib tries to open a window — which fails in terminals without a display (WSL, SSH, CI).

## Your task

Open `task.py`. Uncomment the TODO blocks one section at a time:

**Chart 1** — HP per round (line chart, two lines: hero and boss)

**Chart 2** — Average damage by class (bar chart)

Both charts are saved to the `plots/` folder in the repo root.

Expected charts:

```
plots/
  hp_chart.png      — two lines crossing as hero and boss trade damage
  damage_chart.png  — three bars: Mage, Rogue, Warrior
```

## Run

```bash
uv run python missions/20_plot_the_results/task.py
```

Then open the files to see the charts:

```bash
open plots/hp_chart.png      # macOS
xdg-open plots/hp_chart.png  # Linux
```

## Check

```bash
uv run python missions/20_plot_the_results/check.py
```

The check runs `task.py` and verifies both PNG files exist and are non-empty.

## Side quest

Use your own Project 04 combat log for Chart 1:

```python
# In task.py, change M18_LOG to point to the root-level combat_log.csv
M18_LOG = Path(__file__).parents[2] / "combat_log.csv"
```

Run the game first if the file doesn't exist yet, then replot.

## Break it

Remove `plt.close()` between Chart 1 and Chart 2. Both datasets get drawn on the same figure — six lines tangled together. `plt.close()` is how you tell Matplotlib "I'm done with this chart, start fresh."

## Real-world translation

`plt.savefig()` is how charts are generated in automated reports, dashboards, and CI pipelines — anywhere a human isn't sitting at a display. The pattern: `matplotlib.use("Agg")` → build chart → `savefig()` → `close()` — is standard across data science and backend reporting.

---

Course complete! Final boss: `projects/05_analytics_report/README.md`
