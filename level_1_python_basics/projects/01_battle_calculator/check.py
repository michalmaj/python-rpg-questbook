import re
import sys
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
PROJECT_ID = "01_battle_calculator"
TASK_PATH = "projects/01_battle_calculator/battle_calculator.py"

# Ground truth — mirrors the class table in the README, not the student's code.
CLASS_STATS = {
    "warrior": {"name": "Warrior", "hp": 120},
    "mage": {"name": "Mage", "hp": 80},
    "rogue": {"name": "Rogue", "hp": 100},
}
MONSTER_DAMAGE = 20
POTION_HEAL = 25


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("projects", {})[PROJECT_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def run_script(inputs: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, TASK_PATH],
        input="\n".join(inputs) + "\n",
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return result.stdout


def _extract(pattern: str, out: str) -> int | None:
    m = re.search(pattern, out)
    return int(m.group(1)) if m else None


def check_class(hero_class: str, use_potion: bool) -> None:
    stats = CLASS_STATS[hero_class]
    out = run_script([hero_class, "yes" if use_potion else "no"])

    assert stats["name"] in out, f"{hero_class}: expected '{stats['name']}' in output\n{out}"

    expected_after_attack = max(0, stats["hp"] - MONSTER_DAMAGE)
    actual_after_attack = _extract(r"Your HP:\s*(-?\d+)", out)
    assert actual_after_attack == expected_after_attack, (
        f"{hero_class}: HP after the monster's attack should be {expected_after_attack} "
        f"(max(0, {stats['hp']} - {MONSTER_DAMAGE})), got {actual_after_attack}\n{out}"
    )

    final_hp = actual_after_attack
    if use_potion:
        expected_after_heal = min(stats["hp"], actual_after_attack + POTION_HEAL)
        actual_after_heal = _extract(r"You healed! HP:\s*(-?\d+)", out)
        assert actual_after_heal == expected_after_heal, (
            f"{hero_class}: HP after the potion should be {expected_after_heal} "
            f"(min({stats['hp']}, {actual_after_attack} + {POTION_HEAL})), "
            f"got {actual_after_heal}\n{out}"
        )
        final_hp = actual_after_heal

    if final_hp > 0:
        assert "stands" in out.lower() or "remaining" in out.lower(), (
            f"{hero_class}: hero survives with {final_hp} HP — expected a survival message\n{out}"
        )
    else:
        assert "fallen" in out.lower(), (
            f"{hero_class}: hero should have fallen at 0 HP — expected a defeat message\n{out}"
        )


def main() -> None:
    # Cover all three classes and both potion branches, not just one of each.
    check_class("warrior", use_potion=False)
    check_class("mage", use_potion=True)
    check_class("rogue", use_potion=True)
    check_class("rogue", use_potion=False)

    # Unknown class → handled gracefully, and must not proceed to a battle
    out = run_script(["bard"])
    assert "bard" in out.lower() or "unknown" in out.lower(), (
        f"unknown class: expected an error message in output\n{out}"
    )
    assert "Battle Summary" not in out, (
        f"an unknown class should stop before the battle summary\n{out}"
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
        raise SystemExit(1)
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
        raise SystemExit(1)
