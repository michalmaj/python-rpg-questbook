import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "11_combat_log"
LOG_FILE = REPO_ROOT / "combat_log.csv"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import task

    assert LOG_FILE.exists(), (
        "combat_log.csv not found — did you open and write to the file?"
    )

    lines = LOG_FILE.read_text().splitlines()

    assert len(lines) == 5, (
        f"combat_log.csv: expected 5 lines (1 header + 4 data rows), got {len(lines)}"
    )
    assert lines[0] == "round,hero_hp,monster_hp,hero_dmg,monster_dmg", (
        f"header line mismatch:\n  expected: round,hero_hp,monster_hp,hero_dmg,monster_dmg\n"
        f"  got:      {lines[0]}"
    )
    assert lines[1] == "1,88,45,15,12", (
        f"round 1 mismatch:\n  expected: 1,88,45,15,12\n  got:      {lines[1]}"
    )
    assert lines[4] == "4,52,0,15,12", (
        f"round 4 mismatch:\n  expected: 4,52,0,15,12\n  got:      {lines[4]}"
    )

    _update_progress("complete")
    print("✅ Mission 11 complete: Combat Log")
    print("   Next mission: level_1_python_basics/missions/12_save_game/README.md")


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
