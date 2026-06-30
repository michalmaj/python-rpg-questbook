import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "13_split_the_game"

sys.path.insert(0, str(Path(__file__).parent))


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    from combat import apply_damage, apply_healing, is_alive

    assert apply_damage(100, 30) == 70, "apply_damage(100, 30): expected 70"
    assert apply_damage(20, 50) == 0, "apply_damage(20, 50): HP cannot go below 0"
    assert apply_healing(70, 20, 100) == 90, "apply_healing(70, 20, 100): expected 90"
    assert apply_healing(90, 20, 100) == 100, "apply_healing(90, 20, 100): expected 100 (capped)"
    assert is_alive(52) is True, "is_alive(52): expected True"
    assert is_alive(0) is False, "is_alive(0): expected False"

    result = subprocess.run(
        ["uv", "run", "python", "missions/13_split_the_game/task.py"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, (
        f"task.py crashed — did you add 'from combat import ...'?\n{result.stderr}"
    )
    assert "Hero HP:" in result.stdout, (
        f"task.py: expected 'Hero HP:' in output\n{result.stdout}"
    )

    _update_progress("complete")
    print("✅ Mission 13 complete: Split the Game")
    print("   Next mission: missions/14_hero_dataclass/README.md")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
