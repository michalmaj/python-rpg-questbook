import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
PROJECT_ID = "01_battle_calculator"
TASK_PATH = "projects/01_battle_calculator/battle_calculator.py"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("projects", {})[PROJECT_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def run_script(inputs: list[str]) -> str:
    result = subprocess.run(
        ["uv", "run", "python", TASK_PATH],
        input="\n".join(inputs) + "\n",
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return result.stdout


def main() -> None:
    # Warrior, no potion: 120 hp - 20 damage = 100 hp → survives
    out = run_script(["warrior", "no"])
    assert "Warrior" in out, f"warrior: expected 'Warrior' in output\n{out}"
    assert "100" in out, f"warrior: expected hp=100 after 20 damage (120 - 20 = 100)\n{out}"
    assert "stands" in out.lower() or "remaining" in out.lower(), (
        f"warrior survives — expected a survival message in output\n{out}"
    )

    # Rogue, yes potion: 100 hp - 20 = 80, heal 25 → 100 (capped at max_hp=100)
    out = run_script(["rogue", "yes"])
    assert "Rogue" in out, f"rogue: expected 'Rogue' in output\n{out}"
    assert "You healed! HP: 100" in out, (
        f"rogue: after healing, expected 'You healed! HP: 100' (80 + 25 = 105, capped to 100)\n{out}"
    )

    # Unknown class → error message
    out = run_script(["bard"])
    assert "bard" in out.lower() or "unknown" in out.lower(), (
        f"unknown class: expected an error message in output\n{out}"
    )

    _update_progress("complete")
    print("✅ Project 01 complete: Battle Calculator")
    print("\n   World 1 is clear! Check your progress:")
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
