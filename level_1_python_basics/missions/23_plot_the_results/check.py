"""Check: Mission 23 — Plot the Results.

This check does not just look for a PNG on disk — a blank or fabricated
image would pass that test. Instead it monkeypatches plt.plot/bar/savefig
before importing task.py, records what was actually passed to them, and
compares that against the real combat_df/avg_damage data loaded
independently. Only then does it confirm the files were actually saved.
"""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]  # level_1_python_basics/, not the git repo root
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "23_plot_the_results"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def _values(arg):
    """Normalize a Series/ndarray/list argument to a plain list for comparison."""
    if hasattr(arg, "tolist"):
        return arg.tolist()
    return list(arg)


def main() -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd

    plot_calls = []
    bar_calls = []
    savefig_calls = []

    real_plot, real_bar, real_savefig = plt.plot, plt.bar, plt.savefig

    def spy_plot(*args, **kwargs):
        plot_calls.append(args)
        return real_plot(*args, **kwargs)

    def spy_bar(*args, **kwargs):
        bar_calls.append(args)
        return real_bar(*args, **kwargs)

    def spy_savefig(*args, **kwargs):
        savefig_calls.append(str(args[0]) if args else str(kwargs.get("fname", "")))
        return real_savefig(*args, **kwargs)

    plt.plot, plt.bar, plt.savefig = spy_plot, spy_bar, spy_savefig
    try:
        import task  # runs task.py's module-level plotting code with the spies active
    finally:
        plt.plot, plt.bar, plt.savefig = real_plot, real_bar, real_savefig

    # --- Ground truth: load the same data independently of task.py ---
    expected_combat = pd.read_csv(task.M21_LOG)
    expected_battles = pd.read_csv(task.M22_LOG)
    expected_avg_damage = expected_battles.groupby("hero_class")["damage_dealt"].mean()

    expected_round = _values(expected_combat["round"])
    expected_hero_hp = _values(expected_combat["hero_hp"])
    expected_boss_hp = _values(expected_combat["boss_hp"])

    # --- Chart 1: line plot must use the real round/hero_hp/boss_hp data ---
    assert len(plot_calls) >= 2, (
        f"Expected at least 2 plt.plot() calls (hero HP and boss HP), got {len(plot_calls)}"
    )

    matched_hero = matched_boss = False
    for args in plot_calls:
        if len(args) >= 2:
            x_vals, y_vals = _values(args[0]), _values(args[1])
        elif len(args) == 1:
            x_vals, y_vals = None, _values(args[0])
        else:
            continue
        if y_vals == expected_hero_hp and (x_vals is None or x_vals == expected_round):
            matched_hero = True
        if y_vals == expected_boss_hp and (x_vals is None or x_vals == expected_round):
            matched_boss = True

    assert matched_hero, (
        "No plt.plot() call matches combat_df['round'] vs combat_df['hero_hp'] — "
        "is the hero HP line plotting the actual column?"
    )
    assert matched_boss, (
        "No plt.plot() call matches combat_df['round'] vs combat_df['boss_hp'] — "
        "is the boss HP line plotting the actual column?"
    )

    # --- Chart 2: bar chart must use avg_damage's index/values ---
    assert len(bar_calls) >= 1, "Expected at least 1 plt.bar() call for the damage-by-class chart"
    bar_args = bar_calls[0]
    assert len(bar_args) >= 2, "plt.bar() should be called as plt.bar(x, height)"
    bar_x = list(bar_args[0]) if not hasattr(bar_args[0], "tolist") else bar_args[0].tolist()
    bar_heights = _values(bar_args[1])
    expected_heights = [round(float(v), 4) for v in expected_avg_damage.values]

    assert list(bar_x) == list(expected_avg_damage.index), (
        f"plt.bar() x-values should be avg_damage.index ({list(expected_avg_damage.index)}), got {bar_x}"
    )
    assert [round(float(v), 4) for v in bar_heights] == expected_heights, (
        f"plt.bar() heights should be avg_damage.values ({expected_heights}), got {bar_heights}"
    )

    # --- Both charts must actually be saved via plt.savefig ---
    assert any("hp_chart.png" in p for p in savefig_calls), (
        "No plt.savefig() call saved to a path containing 'hp_chart.png'"
    )
    assert any("damage_chart.png" in p for p in savefig_calls), (
        "No plt.savefig() call saved to a path containing 'damage_chart.png'"
    )

    # --- And the files genuinely exist with real content ---
    hp_chart = REPO_ROOT / "plots" / "hp_chart.png"
    damage_chart = REPO_ROOT / "plots" / "damage_chart.png"
    assert hp_chart.exists() and hp_chart.stat().st_size > 1_000, (
        "plots/hp_chart.png is missing or looks empty"
    )
    assert damage_chart.exists() and damage_chart.stat().st_size > 1_000, (
        "plots/damage_chart.png is missing or looks empty"
    )

    _update_progress("complete")
    print("✅ Mission 23 complete: Plot the Results")
    print(f"   Charts saved to: {REPO_ROOT / 'plots'}")
    print("   Course complete!")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
        raise SystemExit(1)
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
        raise SystemExit(1)
