import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
PROJECT_ID = "03_terminal_rpg"
TASK_PATH = "projects/03_terminal_rpg/rpg.py"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("projects", {})[PROJECT_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def run_script(hero_class: str) -> str:
    result = subprocess.run(
        ["uv", "run", "python", TASK_PATH],
        input=hero_class + "\n",
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return result.stdout


def main() -> None:
    # Warrior run — class selection, combat loop, and ending message
    out = run_script("warrior")
    assert "Warrior" in out, (
        f"warrior: expected 'Warrior' in output\n{out}"
    )
    assert "Round" in out, (
        f"warrior: expected round-by-round output — "
        f"did you implement the while loop?\n{out}"
    )
    assert "wins" in out.lower() or "fallen" in out.lower(), (
        f"warrior: expected 'wins' or 'fallen' in output — "
        f"did you implement the ending message?\n{out}"
    )

    # Mage run — different class works too
    out = run_script("mage")
    assert "Mage" in out, f"mage: expected 'Mage' in output\n{out}"
    assert "Round" in out, f"mage: expected round-by-round output\n{out}"

    # Rogue run
    out = run_script("rogue")
    assert "Rogue" in out, f"rogue: expected 'Rogue' in output\n{out}"

    # Unknown class — handled gracefully
    out = run_script("dragon")
    assert "dragon" in out.lower() or "unknown" in out.lower(), (
        f"unknown class: expected an error message\n{out}"
    )

    _update_progress("complete")
    print("✅ Project 03 complete: Terminal RPG")
    print("\n   World 3 is clear! Check your progress:")
    print("   uv run python tools/course_status.py")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
