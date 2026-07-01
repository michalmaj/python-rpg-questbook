import sys
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "03_choose_your_hero"
TASK_PATH = "missions/03_choose_your_hero/task.py"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def run_task(choice: str) -> str:
    result = subprocess.run(
        [sys.executable, TASK_PATH],
        input=choice + "\n",
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return result.stdout


def main() -> None:
    warrior_out = run_task("warrior")
    assert "Warrior" in warrior_out, f'warrior: expected "Warrior" in output\n{warrior_out}'
    assert "120" in warrior_out, f"warrior: expected hp=120 in output\n{warrior_out}"
    assert "15" in warrior_out, f"warrior: expected damage=15 in output\n{warrior_out}"
    assert "armor" in warrior_out, f'warrior: expected bonus="armor" in output\n{warrior_out}'

    mage_out = run_task("mage")
    assert "Mage" in mage_out, f'mage: expected "Mage" in output\n{mage_out}'
    assert "80" in mage_out, f"mage: expected hp=80 in output\n{mage_out}"
    assert "25" in mage_out, f"mage: expected damage=25 in output\n{mage_out}"
    assert "spell" in mage_out, f'mage: expected bonus="spell" in output\n{mage_out}'

    rogue_out = run_task("rogue")
    assert "Rogue" in rogue_out, f'rogue: expected "Rogue" in output\n{rogue_out}'
    assert "100" in rogue_out, f"rogue: expected hp=100 in output\n{rogue_out}"
    assert "20" in rogue_out, f"rogue: expected damage=20 in output\n{rogue_out}"
    assert "crit" in rogue_out, f'rogue: expected bonus="crit" in output\n{rogue_out}'

    unknown_out = run_task("wizard")
    assert "wizard" in unknown_out.lower() or "unknown" in unknown_out.lower(), (
        f"unknown class: expected an error message in output\n{unknown_out}"
    )

    _update_progress("complete")
    print("✅ Mission 03 complete: Choose Your Hero")
    print("   Next up: level_1_python_basics/projects/01_battle_calculator/README.md")


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
