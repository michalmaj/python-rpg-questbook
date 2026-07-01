import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "10_safe_input"
TASK_PATH = "missions/10_safe_input/task.py"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def run_task(user_input: str) -> str:
    result = subprocess.run(
        ["uv", "run", "python", TASK_PATH],
        input=user_input + "\n",
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return result.stdout


def main() -> None:
    # Valid number → use it directly
    out = run_task("75")
    assert "Monster HP: 75" in out, (
        f"valid input '75': expected 'Monster HP: 75' in output\n{out}"
    )

    # Invalid text → fall back to default 100
    out = run_task("banana")
    assert "Monster HP: 100" in out, (
        f"invalid input 'banana': expected 'Monster HP: 100' (default) in output\n{out}"
    )

    # Another invalid input → also falls back to 100
    out = run_task("twelve")
    assert "Monster HP: 100" in out, (
        f"invalid input 'twelve': expected 'Monster HP: 100' (default) in output\n{out}"
    )

    _update_progress("complete")
    print("✅ Mission 10 complete: Safe Input")
    print("   Next up: projects/03_terminal_rpg/README.md")


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
