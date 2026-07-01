import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
PROJECT_ID = "02_turn_based_combat"
TASK_PATH = REPO_ROOT / "projects" / "02_turn_based_combat" / "task.py"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("projects", {})[PROJECT_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    result = subprocess.run(
        [sys.executable, str(TASK_PATH)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"task.py crashed — check for syntax errors:\n{result.stderr}"
    )

    out = result.stdout

    assert "enters the Arena" in out, (
        "Hero intro line not found — did you keep the opening print()?"
    )
    assert "Round 1" in out, (
        "'Round 1' not in output — is your while loop running?"
    )
    assert "falls!" in out or "fell" in out, (
        "No enemy was defeated or killed — check your while loop condition"
    )
    assert "Battle Summary" in out, (
        "'Battle Summary' not found — is your for loop over battle_log printing?"
    )
    assert "Defeated" in out or "Fell" in out, (
        "Battle log appears empty — did you append() results to battle_log?"
    )
    assert "Potions remaining:" in out, (
        "'Potions remaining:' not found — did you print the potions count at the end?"
    )

    _update_progress("complete")
    print(result.stdout)
    print("✅ Project 02 complete: Turn-Based Combat Arena")
    print()
    print("   for loop, while loop, lists — all three in one fight.")
    print()
    print("   World 2 is clear! Check your progress:")
    print("   uv run python tools/course_status.py")


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
