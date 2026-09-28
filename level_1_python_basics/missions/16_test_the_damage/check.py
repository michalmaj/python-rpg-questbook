import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "16_test_the_damage"
MISSION_DIR = Path(__file__).parent
COMBAT_FILE = MISSION_DIR / "combat.py"
TEST_FILE = "missions/16_test_the_damage/test_combat.py"

# Three independent mutants, each breaking exactly one behavior while the
# other two functions stay correct. A test suite only has to notice one
# bug per mutant, but it has to notice ALL THREE mutants — one true test
# plus five tautologies can kill at most one of these, which is the exact
# gap this gate closes versus a single combined mutant.

MUTANT_A_NO_DAMAGE_FLOOR = '''def apply_damage(hp, damage):
    return hp - damage  # bug: no floor at 0


def apply_healing(hp, heal_amount, max_hp):
    return min(max_hp, hp + heal_amount)


def is_alive(hp):
    return hp > 0
'''

MUTANT_B_NO_HEAL_CAP = '''def apply_damage(hp, damage):
    return max(0, hp - damage)


def apply_healing(hp, heal_amount, max_hp):
    return hp + heal_amount  # bug: no cap at max_hp


def is_alive(hp):
    return hp > 0
'''

MUTANT_C_ALIVE_BOUNDARY = '''def apply_damage(hp, damage):
    return max(0, hp - damage)


def apply_healing(hp, heal_amount, max_hp):
    return min(max_hp, hp + heal_amount)


def is_alive(hp):
    return hp >= 0  # bug: 0 HP counts as alive
'''

MUTANTS = [
    ("A", "no floor on apply_damage (HP can go negative)", MUTANT_A_NO_DAMAGE_FLOOR),
    ("B", "no cap on apply_healing (HP can exceed max_hp)", MUTANT_B_NO_HEAL_CAP),
    ("C", "is_alive(0) wrongly returns True", MUTANT_C_ALIVE_BOUNDARY),
]


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


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
        [sys.executable, "-m", "pytest", TEST_FILE, "-v"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )


def _run_against_mutant(original: str, mutant_source: str) -> subprocess.CompletedProcess:
    """Swap combat.py for `mutant_source`, run the student's tests, then put
    the original content back — unconditionally, even if pytest itself
    errors out. Never leaves combat.py mutated."""
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

    assert result.returncode == 0, (
        "Some tests are still failing — replace every ... with the expected value."
    )
    assert "6 passed" in result.stdout, (
        "Expected 6 tests to pass — check the output above."
    )

    # ── Gate 2: the tests must catch each of three independent bugs ──
    # One real test buried among five tautologies can kill at most one
    # mutant — this loop requires all three to die, each on its own.
    try:
        for label, description, mutant_source in MUTANTS:
            mutant_result = _run_against_mutant(original_combat, mutant_source)
            assert mutant_result.returncode != 0, (
                f"Your tests still all pass against mutant {label} — {description}. "
                "No test in your suite catches this specific bug. A tautology like "
                "`assert result == result` (or a test that only covers a different "
                "behavior) won't catch it — assert the actual expected value for "
                "this case."
            )
    finally:
        # Belt-and-braces: guarantee combat.py is exactly as it started,
        # even if something above raised before its own restore ran.
        COMBAT_FILE.write_text(original_combat)

    assert COMBAT_FILE.read_text() == original_combat, (
        "combat.py was not restored correctly — this is a checker bug, not "
        "something in your solution. Please report it."
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
