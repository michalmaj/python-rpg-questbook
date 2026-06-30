import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "15_test_the_damage"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    result = subprocess.run(
        ["uv", "run", "pytest", "missions/15_test_the_damage/test_combat.py", "-v"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )

    print(result.stdout)

    assert result.returncode == 0, (
        "Some tests are still failing — replace every ... with the expected value."
    )
    assert "6 passed" in result.stdout, (
        "Expected 6 tests to pass — check the output above."
    )

    _update_progress("complete")
    print("✅ Mission 15 complete: Test the Damage")
    print("   World 4 done! Next: projects/04_full_rpg/README.md")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
