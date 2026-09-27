import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "16_test_the_damage"
MISSION_DIR = Path(__file__).parent
COMBAT_FILE = MISSION_DIR / "combat.py"
TEST_FILE = "missions/16_test_the_damage/test_combat.py"

# A deliberately broken combat.py, used only to prove the student's tests
# check real values instead of a tautology like `assert result == result`
# (which would pass against this too). Restored immediately after use.
MUTANT_COMBAT = '''def apply_damage(hp, damage):
    return hp - damage  # bug: no floor at 0


def apply_healing(hp, heal_amount, max_hp):
    return hp + heal_amount  # bug: no cap at max_hp


def is_alive(hp):
    return hp >= 0  # bug: 0 HP counts as alive
'''


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def _run_pytest() -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "pytest", TEST_FILE, "-v"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def main() -> None:
    # ── Gate 1: tests pass against the real, correct combat.py ──
    result = _run_pytest()
    print(result.stdout)

    assert result.returncode == 0, (
        "Some tests are still failing — replace every ... with the expected value."
    )
    assert "6 passed" in result.stdout, (
        "Expected 6 tests to pass — check the output above."
    )

    # ── Gate 2: the tests must actually catch a broken implementation ──
    # Temporarily swap in a combat.py with three realistic bugs (no HP floor,
    # no healing cap, 0 HP counted as alive), then rerun the SAME tests.
    # A test like `assert result == result` passes no matter what combat.py
    # does, so if every test still passes here, they weren't checking
    # anything real. combat.py is restored immediately either way.
    original_combat = COMBAT_FILE.read_text()
    try:
        COMBAT_FILE.write_text(MUTANT_COMBAT)
        mutant_result = _run_pytest()
    finally:
        COMBAT_FILE.write_text(original_combat)

    assert mutant_result.returncode != 0, (
        "Your tests still all pass even against a deliberately broken "
        "combat.py (no HP floor, no healing cap, 0 HP treated as alive). "
        "That means they aren't checking real values — replace any "
        "tautology like `assert result == result` with the actual number "
        "you expect."
    )

    _update_progress("complete")
    print("✅ Mission 16 complete: Test the Damage")
    print("   World 4 done! Next: projects/04_full_rpg/README.md")


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
