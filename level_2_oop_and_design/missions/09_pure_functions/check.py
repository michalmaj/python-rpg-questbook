"""check.py — Mission 09: Pure Functions"""

import io
import json
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]
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
    try:
        from task import compute_damage, resolve_hit
    except ImportError as e:
        print(f"❌ Could not import compute_damage and resolve_hit from task.py: {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Error in task.py: {e}")
        raise SystemExit(1)

    try:
        # compute_damage is deterministic
        assert compute_damage(15, 5, 4) == 14, \
            f"compute_damage(15, 5, 4) should be 14, got {compute_damage(15, 5, 4)}"
        assert compute_damage(10, 3, 6) == 13, \
            f"compute_damage(10, 3, 6) should be 13, got {compute_damage(10, 3, 6)}"

        # Minimum 1
        assert compute_damage(1, 100, 1) == 1, \
            "compute_damage should never return less than 1"
        assert compute_damage(5, 20, 1) == 1, \
            "compute_damage(5, 20, 1) should be 1 (floored), got " \
            f"{compute_damage(5, 20, 1)}"

        # compute_damage does NOT print
        buf = io.StringIO()
        with redirect_stdout(buf):
            compute_damage(15, 5, 4)
        output = buf.getvalue()
        assert output == "", \
            f"compute_damage should not print anything, but it printed: {output!r}"

        # resolve_hit returns a positive int
        for _ in range(10):
            dmg = resolve_hit(15, 5)
            assert isinstance(dmg, int) and dmg >= 1, \
                f"resolve_hit should return int >= 1, got {dmg!r}"

        # resolve_hit does NOT print
        buf2 = io.StringIO()
        with redirect_stdout(buf2):
            resolve_hit(15, 5)
        assert buf2.getvalue() == "", \
            "resolve_hit should not print anything"

        # resolve_hit range: atk=15, def=5 → base=10, plus d6 (1-6) → 11-16
        results = {resolve_hit(15, 5) for _ in range(200)}
        assert all(11 <= r <= 16 for r in results), \
            f"resolve_hit(15, 5) should return 11-16, got values: {sorted(results)}"

    except AssertionError as e:
        print(f"❌ {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise SystemExit(1)

    update_progress("09_pure_functions")
    print("✅ Mission 09 complete: Damage logic extracted into pure functions!")
    print()
    print("   compute_damage(15, 5, 4) == 14 — deterministic, no randomness, no side effects.")
    print("   Next mission: level_2_oop_and_design/missions/10_add_tests/README.md")


if __name__ == "__main__":
    main()
