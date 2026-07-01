import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
PROJECT_ID = "05_analytics_report"

HP_CHART = REPO_ROOT / "plots" / "report_hp.png"
DAMAGE_CHART = REPO_ROOT / "plots" / "report_damage.png"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("projects", {})[PROJECT_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    result = subprocess.run(
        ["uv", "run", "python", "projects/05_analytics_report/analytics.py"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )

    assert result.returncode == 0, (
        f"analytics.py crashed — complete all TODOs before running check:\n{result.stderr}"
    )

    out = result.stdout
    assert "GAME ANALYTICS REPORT" in out, "'GAME ANALYTICS REPORT' not in output"
    assert "REPORT COMPLETE" in out, "'REPORT COMPLETE' not in output — did the script finish?"
    assert "Avg hero HP:" in out, "'Avg hero HP:' not in output — did you complete Section 1?"
    assert "Warrior d6" in out, "'Warrior d6' not in output — did you complete Section 2?"
    assert "Avg damage by class:" in out, "'Avg damage by class:' not in output — did you complete Section 3?"

    assert HP_CHART.exists(), (
        "plots/report_hp.png not found — did you complete the Chart 1 TODO?"
    )
    assert HP_CHART.stat().st_size > 5_000, (
        "plots/report_hp.png looks empty — check your plt.plot() and plt.savefig() calls"
    )

    assert DAMAGE_CHART.exists(), (
        "plots/report_damage.png not found — did you complete the Chart 2 TODO?"
    )
    assert DAMAGE_CHART.stat().st_size > 5_000, (
        "plots/report_damage.png looks empty — check your plt.bar() and plt.savefig() calls"
    )

    _update_progress("complete")
    print(result.stdout)
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
