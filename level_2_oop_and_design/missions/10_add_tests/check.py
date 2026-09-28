"""check.py — Mission 10: Add Tests"""

import ast
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]
MISSION_DIR = Path(__file__).parent
PROGRESS_FILE = REPO_ROOT / "level_2_oop_and_design" / ".progress"
COMBAT_FILE = MISSION_DIR / "combat.py"
TEST_FILE = MISSION_DIR / "test_combat.py"

# combat.py is "provided and complete" for this mission, so the only way to
# tell a real test suite from five tautologies (`assert True`, `assert x ==
# x`) is to see whether it actually catches broken behaviour. Each mutant
# below breaks exactly one thing the mission's five tests are meant to
# cover — a suite that passes against ALL of them was never really testing
# anything.

MUTANT_NO_FLOOR = '''import random


def compute_damage(atk: int, def_: int, dice_roll: int) -> int:
    return atk + dice_roll - def_  # bug: no floor at 1


def resolve_hit(atk: int, def_: int) -> int:
    return compute_damage(atk, def_, random.randint(1, 6))
'''

MUTANT_DEFENCE_IGNORED = '''import random


def compute_damage(atk: int, def_: int, dice_roll: int) -> int:
    return max(1, atk + dice_roll)  # bug: def_ has no effect


def resolve_hit(atk: int, def_: int) -> int:
    return compute_damage(atk, def_, random.randint(1, 6))
'''

MUTANT_ATTACK_IGNORED = '''import random


def compute_damage(atk: int, def_: int, dice_roll: int) -> int:
    return max(1, dice_roll - def_)  # bug: atk has no effect


def resolve_hit(atk: int, def_: int) -> int:
    return compute_damage(atk, def_, random.randint(1, 6))
'''

MUTANT_ROLL_IGNORED = '''import random


def compute_damage(atk: int, def_: int, dice_roll: int) -> int:
    return max(1, atk + 1 - def_)  # bug: dice_roll has no effect


def resolve_hit(atk: int, def_: int) -> int:
    return compute_damage(atk, def_, random.randint(1, 6))
'''

MUTANT_ZERO_DEFENCE_BUG = '''import random


def compute_damage(atk: int, def_: int, dice_roll: int) -> int:
    if def_ == 0:
        return max(1, atk + dice_roll - 1)  # bug: off-by-one only when def_ == 0
    return max(1, atk + dice_roll - def_)


def resolve_hit(atk: int, def_: int) -> int:
    return compute_damage(atk, def_, random.randint(1, 6))
'''

MUTANTS = [
    ("no floor at 1", "compute_damage(1, 100, 1) should be 1, not a negative number", MUTANT_NO_FLOOR),
    ("defence ignored", "higher def_ should reduce damage", MUTANT_DEFENCE_IGNORED),
    ("attack ignored", "higher atk should increase damage", MUTANT_ATTACK_IGNORED),
    ("dice roll ignored", "a higher dice_roll should increase damage", MUTANT_ROLL_IGNORED),
    ("zero-defence bug", "compute_damage(10, 0, 5) should be 15", MUTANT_ZERO_DEFENCE_BUG),
]


def update_progress(mission_id: str) -> None:
    progress: dict = {"missions": {}, "projects": {}}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    progress["missions"][mission_id] = "complete"
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


def _clear_pycache() -> None:
    # combat.py gets rewritten several times in quick succession below. If
    # two writes land within the same mtime tick, Python's import system can
    # reuse a stale cached .pyc instead of recompiling — silently testing
    # the wrong version of combat.py. PYTHONDONTWRITEBYTECODE stops new
    # stale caches from being written; clearing first removes any leftover
    # from an earlier run (e.g. the student running pytest by hand).
    cache_dir = MISSION_DIR / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)


def _run_pytest() -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run(
        [sys.executable, "-m", "pytest", str(TEST_FILE), "-v", "--tb=short"],
        capture_output=True,
        text=True,
        cwd=str(MISSION_DIR),
        env=env,
    )


def _run_against_mutant(original: str, mutant_source: str) -> subprocess.CompletedProcess:
    """Swap combat.py for mutant_source, run the student's tests, then
    restore the original — unconditionally, even if pytest itself errors."""
    try:
        _clear_pycache()
        COMBAT_FILE.write_text(mutant_source)
        return _run_pytest()
    finally:
        COMBAT_FILE.write_text(original)


def main() -> None:
    original_combat = COMBAT_FILE.read_text()

    # ── Gate 1: tests pass against the real, correct combat.py ──
    _clear_pycache()
    result = _run_pytest()
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        print("❌ Some tests are failing or incomplete. Fix test_combat.py and try again.")
        raise SystemExit(1)

    # Sanity check: real assert statements, not just `pass`
    test_source = TEST_FILE.read_text()
    try:
        tree = ast.parse(test_source)
    except SyntaxError as e:
        print(f"❌ test_combat.py has a syntax error: {e}")
        raise SystemExit(1)
    assert_count = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
    if assert_count < 5:
        print(f"❌ Found only {assert_count} real assert statement(s) in test_combat.py.")
        print("   Each test function needs at least one assert. Replace 'pass' with an assert.")
        raise SystemExit(1)

    # ── Gate 2: the tests must independently catch five distinct bugs ──
    # "At least one test fails" is not enough — a single real assertion
    # buried among tautologies could kill one mutant and let the other four
    # survive. Every mutant below has to fail the suite on its own.
    try:
        for label, hint, mutant_source in MUTANTS:
            mutant_result = _run_against_mutant(original_combat, mutant_source)
            if mutant_result.returncode == 0:
                print(mutant_result.stdout)
                print(
                    f"❌ Your tests still all pass against a combat.py with a "
                    f"deliberate bug ({label}) — {hint}. That means no test in "
                    f"your suite actually checks this behavior with a real "
                    f"expected value."
                )
                raise SystemExit(1)
    finally:
        # Belt-and-braces: guarantee combat.py is exactly as it started,
        # even if something above raised before its own restore ran.
        COMBAT_FILE.write_text(original_combat)

    if COMBAT_FILE.read_text() != original_combat:
        print(
            "❌ combat.py was not restored correctly — this is a checker bug, "
            "not something in your solution. Please report it."
        )
        raise SystemExit(1)

    update_progress("10_add_tests")
    print("✅ Mission 10 complete: All tests pass!")
    print()
    print("   Tests are your safety net. Every change you make, they catch regressions.")
    print()
    print("   You finished all 10 missions. Time for the boss fight:")
    print("   level_2_oop_and_design/projects/03_refactored_rpg/README.md")


if __name__ == "__main__":
    main()
