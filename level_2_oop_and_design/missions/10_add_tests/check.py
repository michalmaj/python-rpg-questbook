"""check.py — Mission 10: Add Tests"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]
MISSION_DIR = Path(__file__).parent
PROGRESS_FILE = REPO_ROOT / "level_2_oop_and_design" / ".progress"


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


def main() -> None:
    result = __import__("subprocess").run(
        [sys.executable, "-m", "pytest", str(MISSION_DIR / "test_combat.py"), "-v", "--tb=short"],
        capture_output=True,
        text=True,
        cwd=str(MISSION_DIR),
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        print("❌ Some tests are failing or incomplete. Fix test_combat.py and try again.")
        raise SystemExit(1)

    # Extra check: make sure students actually wrote real assert statements (not just comments or pass)
    import ast
    test_source = (MISSION_DIR / "test_combat.py").read_text()
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

    update_progress("10_add_tests")
    print("✅ Mission 10 complete: All tests pass!")
    print()
    print("   Tests are your safety net. Every change you make, they catch regressions.")
    print()
    print("   You finished all 10 missions. Time for the boss fight:")
    print("   level_2_oop_and_design/projects/01_refactored_rpg/README.md")


if __name__ == "__main__":
    main()
