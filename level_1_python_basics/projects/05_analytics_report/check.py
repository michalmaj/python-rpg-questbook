"""Check: Project 05 — Game Analytics Report.

Imports the student's functions directly and calls them with:
  (a) a small synthetic dataset built here, with hand-computable answers —
      this is what proves the LOGIC is right, independent of the real data;
  (b) the real M21/M22 data files — an integration sanity check;
  (c) a behavioral spy on the plotting calls, same technique as Mission 23.

Nothing here depends on the student's internal variable names — only the
function names/signatures declared in analytics.py are the contract.
"""
import json
from io import StringIO
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]  # level_1_python_basics/, not the git repo root
PROGRESS_FILE = REPO_ROOT / ".progress"
PROJECT_ID = "05_analytics_report"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("projects", {})[PROJECT_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


SYNTHETIC_BATTLES_CSV = """hero_name,hero_class,damage_dealt,victory
A,X,10,1
B,X,20,1
C,Y,25,0
D,Y,35,0
"""

SYNTHETIC_COMBAT_CSV = """round,hero_hp,boss_hp
1,50,90
2,30,70
3,10,50
4,40,20
"""


def _values(arg):
    """Normalize a Series/ndarray/list argument to a plain list for comparison."""
    if hasattr(arg, "tolist"):
        return arg.tolist()
    return list(arg)


def _line_series(args):
    """Parse one plt.plot(...) call's positional args into (x, y) pairs.

    Handles plt.plot(y), plt.plot(x, y), and plt.plot(x1, y1, x2, y2, ...) —
    matplotlib's own "groups of 2 (or 3 with a format string)" convention.
    A trailing style string like "ro-" is dropped; real coordinate data is
    never a bare str.
    """
    data_args = [a for a in args if not isinstance(a, str)]
    series = []
    i = 0
    while i < len(data_args):
        if i + 1 < len(data_args):
            series.append((_values(data_args[i]), _values(data_args[i + 1])))
            i += 2
        else:
            series.append((None, _values(data_args[i])))
            i += 1
    return series


def _bar_xy(args, kwargs):
    """Extract (x, height) from a plt.bar(...) call — positional or keyword."""
    x = args[0] if len(args) >= 1 else kwargs.get("x")
    height = args[1] if len(args) >= 2 else kwargs.get("height")
    return _values(x), _values(height)


def main() -> None:
    import numpy as np
    import pandas as pd
    import analytics

    synth_battles = pd.read_csv(StringIO(SYNTHETIC_BATTLES_CSV))
    synth_combat = pd.read_csv(StringIO(SYNTHETIC_COMBAT_CSV))

    # ── Q1: avg_damage_by_class — synthetic (hand-computable) ──
    avg_synth = analytics.avg_damage_by_class(synth_battles)
    assert isinstance(avg_synth, pd.Series), (
        f"avg_damage_by_class should return a Series, got {type(avg_synth).__name__}"
    )
    assert abs(avg_synth["X"] - 15.0) < 0.01, f"avg_damage_by_class: X should be 15.0, got {avg_synth['X']}"
    assert abs(avg_synth["Y"] - 30.0) < 0.01, f"avg_damage_by_class: Y should be 30.0, got {avg_synth['Y']}"

    # ── Q2: count_above_threshold — synthetic ──
    count_synth = analytics.count_above_threshold(synth_battles, 15)
    assert count_synth == 3, f"count_above_threshold(threshold=15): expected 3 (B, C, D), got {count_synth}"
    assert analytics.count_above_threshold(synth_battles, 100) == 0, (
        "count_above_threshold(threshold=100): expected 0 — nobody dealt that much"
    )

    # ── Q3: damage_distribution — checked against NumPy's own ground truth ──
    sample = np.array([10, 20, 25, 35, 40])
    stats = analytics.damage_distribution(sample)
    assert isinstance(stats, dict), f"damage_distribution should return a dict, got {type(stats).__name__}"
    for key in ("mean", "std", "p25", "p75"):
        assert key in stats, f"damage_distribution result is missing '{key}'"
    assert abs(stats["mean"] - float(np.mean(sample))) < 0.01, (
        f"damage_distribution: mean should be {np.mean(sample):.2f}, got {stats['mean']}"
    )
    assert abs(stats["std"] - float(np.std(sample))) < 0.01, (
        f"damage_distribution: std should be {np.std(sample):.2f}, got {stats['std']}"
    )
    assert abs(stats["p25"] - float(np.percentile(sample, 25))) < 0.01, (
        f"damage_distribution: p25 should be {np.percentile(sample, 25):.2f}, got {stats['p25']}"
    )
    assert abs(stats["p75"] - float(np.percentile(sample, 75))) < 0.01, (
        f"damage_distribution: p75 should be {np.percentile(sample, 75):.2f}, got {stats['p75']}"
    )

    # ── Q4: win_rate_by_class — synthetic ──
    wr_synth = analytics.win_rate_by_class(synth_battles)
    assert abs(wr_synth["X"] - 1.0) < 0.01, f"win_rate_by_class: X should be 1.0 (both won), got {wr_synth['X']}"
    assert abs(wr_synth["Y"] - 0.0) < 0.01, f"win_rate_by_class: Y should be 0.0 (both lost), got {wr_synth['Y']}"

    # ── Bonus: top_damage_hero — synthetic ──
    assert analytics.top_damage_hero(synth_battles) == "D", (
        f"top_damage_hero: expected 'D' (35 damage), got {analytics.top_damage_hero(synth_battles)!r}"
    )

    # ── Q5: lowest_hp_round — synthetic (non-monotonic on purpose) ──
    assert analytics.lowest_hp_round(synth_combat) == 3, (
        f"lowest_hp_round: expected round 3 (hp=10, the actual minimum — not just the "
        f"last row), got {analytics.lowest_hp_round(synth_combat)}"
    )

    # ── Integration sanity check: the real M21/M22 data ──
    real_combat = analytics.load_combat_log(analytics.M21_LOG)
    real_battles = analytics.load_battles(analytics.M22_LOG)
    real_avg = analytics.avg_damage_by_class(real_battles)
    assert abs(real_avg["Warrior"] - 155.0) < 0.1, (
        f"avg_damage_by_class on the real data: Warrior should be ~155.0, got {real_avg['Warrior']}"
    )
    assert analytics.top_damage_hero(real_battles) == "Brom", (
        f"top_damage_hero on the real data: expected 'Brom', got {analytics.top_damage_hero(real_battles)!r}"
    )
    assert analytics.count_above_threshold(real_battles, 150) == 4, (
        f"count_above_threshold(150) on the real data: expected 4, "
        f"got {analytics.count_above_threshold(real_battles, 150)}"
    )

    # ── Q6: plotting — behavioral spy, same approach as Mission 23 ──
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plot_calls, bar_calls, savefig_calls = [], [], []
    real_plot, real_bar, real_savefig = plt.plot, plt.bar, plt.savefig

    def spy_plot(*args, **kwargs):
        plot_calls.append((args, kwargs))
        return real_plot(*args, **kwargs)

    def spy_bar(*args, **kwargs):
        bar_calls.append((args, kwargs))
        return real_bar(*args, **kwargs)

    def spy_savefig(*args, **kwargs):
        savefig_calls.append(str(args[0]) if args else str(kwargs.get("fname", "")))
        return real_savefig(*args, **kwargs)

    plt.plot, plt.bar, plt.savefig = spy_plot, spy_bar, spy_savefig
    try:
        hp_path = REPO_ROOT / "plots" / "_check_hp.png"
        dmg_path = REPO_ROOT / "plots" / "_check_damage.png"
        analytics.plot_hp_over_time(real_combat, hp_path)
        analytics.plot_avg_damage_by_class(real_avg, dmg_path)
    finally:
        plt.plot, plt.bar, plt.savefig = real_plot, real_bar, real_savefig

    expected_hero_hp = _values(real_combat["hero_hp"])
    expected_boss_hp = _values(real_combat["boss_hp"])

    # One call can draw more than one line (plt.plot(x, y1, x, y2)), so every
    # (x, y) pair across every call is a candidate — not just one per call.
    all_series = []
    for args, _kwargs in plot_calls:
        all_series.extend(_line_series(args))

    matched_hero = any(y == expected_hero_hp for _x, y in all_series)
    matched_boss = any(y == expected_boss_hp for _x, y in all_series)
    assert matched_hero, "plot_hp_over_time: no line used the real hero_hp column"
    assert matched_boss, "plot_hp_over_time: no line used the real boss_hp column"

    assert len(bar_calls) >= 1, "plot_avg_damage_by_class: expected at least one plt.bar() call"
    bar_x, bar_heights = _bar_xy(*bar_calls[0])
    assert bar_x == list(real_avg.index), (
        f"plot_avg_damage_by_class: bar x-values should be avg_damage.index, got {bar_x}"
    )
    assert [round(v, 4) for v in bar_heights] == [round(float(v), 4) for v in real_avg.values], (
        "plot_avg_damage_by_class: bar heights should be avg_damage.values"
    )

    assert any("_check_hp.png" in p for p in savefig_calls), (
        "plot_hp_over_time did not call plt.savefig() with the given save_path"
    )
    assert any("_check_damage.png" in p for p in savefig_calls), (
        "plot_avg_damage_by_class did not call plt.savefig() with the given save_path"
    )
    assert hp_path.exists() and hp_path.stat().st_size > 1_000, "the HP chart file looks empty"
    assert dmg_path.exists() and dmg_path.stat().st_size > 1_000, "the damage chart file looks empty"

    _update_progress("complete")
    print("✅ Project 05 complete: Game Analytics Report")
    print()
    print("   You built a terminal RPG and analyzed it with Python.")
    print("   NumPy, Pandas, Matplotlib — you used all three.")
    print("   Course complete.")


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
