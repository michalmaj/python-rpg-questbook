import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "20_plot_the_results"

HP_CHART = REPO_ROOT / "plots" / "hp_chart.png"
DAMAGE_CHART = REPO_ROOT / "plots" / "damage_chart.png"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    result = subprocess.run(
        ["uv", "run", "python", "missions/20_plot_the_results/task.py"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, (
        f"task.py crashed:\n{result.stderr}"
    )

    assert HP_CHART.exists(), (
        "plots/hp_chart.png not found — did you uncomment plt.savefig(PLOTS_DIR / 'hp_chart.png')?"
    )
    assert HP_CHART.stat().st_size > 5_000, (
        f"plots/hp_chart.png looks empty ({HP_CHART.stat().st_size} bytes) — "
        "did you uncomment the plt.plot() and plt.savefig() lines?"
    )

    assert DAMAGE_CHART.exists(), (
        "plots/damage_chart.png not found — did you uncomment the Chart 2 block?"
    )
    assert DAMAGE_CHART.stat().st_size > 5_000, (
        f"plots/damage_chart.png looks empty ({DAMAGE_CHART.stat().st_size} bytes)"
    )

    _update_progress("complete")
    print("✅ Mission 20 complete: Plot the Results")
    print(f"   Charts saved to: {REPO_ROOT / 'plots'}")
    print("   Final boss next: projects/05_analytics_report/README.md")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
